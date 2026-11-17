#!/usr/bin/env python3
"""Inventory every DAT_xxxxxxxx global referenced by the decompiled sources.

Scans .cpp .h .hpp .inl files under the input roots (read once each), records
extern declarations / file-scope definitions / reference counts per address,
and maps each address onto the PE sections of the reference image (read-only).

Outputs (under runtime-next/m3/inventory):
  dat_globals.json        per-address records
  dat_globals_summary.txt short human-readable summary
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

RN = r"C:\Projects\Decompilation\runtime-next"
sys.path.append(RN)
import paths  # noqa: E402  (shared path config, read-only use)

PY_SITE = getattr(paths, "PY_SITE", None)
if PY_SITE and os.path.isdir(PY_SITE) and PY_SITE not in sys.path:
    sys.path.append(PY_SITE)
import pefile  # noqa: E402

PROJ = paths.PROJ
REF_IMAGE = paths.REF_IMAGE
OUT_DIR = os.path.join(RN, "m3", "inventory")

INPUT_ROOTS = [
    os.path.join(PROJ, "fnv_decomp", "src"),
    os.path.join(PROJ, "fnv_decomp", "include"),
    os.path.join(PROJ, "FNV", "contributions"),
]
# Never scanned, even if they sit under an input root.
FORBIDDEN = [
    os.path.join(PROJ, "FNV", "work"),
    os.path.join(PROJ, "FNV", "local"),
    os.path.join(PROJ, "fnv_decomp", "build", "rebuild"),
]
EXTS = (".cpp", ".h", ".hpp", ".inl")
MAX_DECLS = 5

DAT_RE = re.compile(r"\bDAT_([0-9a-fA-F]{8})\b")
ADDR_OF_RE = re.compile(r"&\s*DAT_([0-9a-fA-F]{8})\b")
EXTERN_RE = re.compile(r"^\s*extern\b")
DEF_RE = re.compile(
    r"^\s*(?:(?:static|const|volatile)\s+)*[A-Za-z_][\w\s\*]*?\s*\bDAT_([0-9a-fA-F]{8})\b"
    r"\s*((?:\[[^\]]*\]\s*)*)(?:=[^;()]*)?;\s*$"
)
STR_RE = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
LINE_COMMENT_RE = re.compile(r"//.*$")


def is_forbidden(path):
    p = os.path.normcase(os.path.abspath(path))
    for f in FORBIDDEN:
        fn = os.path.normcase(os.path.abspath(f))
        if p == fn or p.startswith(fn + os.sep):
            return True
    return False


def iter_source_files():
    for root in INPUT_ROOTS:
        if is_forbidden(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            # prune forbidden subtrees before descending
            dirnames[:] = [d for d in dirnames
                           if not is_forbidden(os.path.join(dirpath, d))]
            for fn in filenames:
                if fn.lower().endswith(EXTS):
                    full = os.path.join(dirpath, fn)
                    if not is_forbidden(full):
                        yield full


def clean_type(text):
    text = re.sub(r'\bextern\b\s*("[^"]*")?', " ", text)
    text = re.sub(r"\bstatic\b", " ", text)
    text = re.sub(r"__declspec\s*\([^)]*\)", " ", text)
    return " ".join(text.split())


def brace_delta(line):
    s = LINE_COMMENT_RE.sub("", STR_RE.sub('""', line))
    return s.count("{") - s.count("}")


def new_rec():
    return {"decls": [], "defs": [], "types": set(), "files": set(),
            "n_refs": 0, "uses_address_of": 0}


def scan():
    recs = defaultdict(new_rec)
    files_scanned = 0
    for path in iter_source_files():
        files_scanned += 1
        with open(path, "rb") as fh:
            text = fh.read().decode("utf-8", errors="replace")
        rel = os.path.relpath(path, PROJ)
        depth = 0
        for line in text.splitlines():
            hits = DAT_RE.findall(line)
            if hits:
                for h in hits:
                    r = recs[h.lower()]
                    r["n_refs"] += 1
                    r["files"].add(rel)
                for h in ADDR_OF_RE.findall(line):
                    recs[h.lower()]["uses_address_of"] += 1

                stripped = " ".join(line.split())
                if EXTERN_RE.match(line) and stripped.endswith(";"):
                    m_first = DAT_RE.search(line)
                    base = clean_type(line[:m_first.start()])
                    for m in DAT_RE.finditer(line):
                        key = m.group(1).lower()
                        r = recs[key]
                        if len(r["decls"]) < MAX_DECLS and stripped not in r["decls"]:
                            r["decls"].append(stripped)
                        suffix_m = re.match(r"\s*((?:\[[^\]]*\]\s*)*)", line[m.end():])
                        suffix = "".join(suffix_m.group(1).split()) if suffix_m else ""
                        if base:
                            r["types"].add(base + suffix)
                elif depth == 0 and "(" not in line:
                    dm = DEF_RE.match(line)
                    if dm:
                        key = dm.group(1).lower()
                        r = recs[key]
                        if len(r["defs"]) < MAX_DECLS and stripped not in r["defs"]:
                            r["defs"].append(stripped)
            depth += brace_delta(line)
            if depth < 0:
                depth = 0
    return recs, files_scanned


def load_sections():
    pe = pefile.PE(REF_IMAGE, fast_load=True)
    try:
        image_base = pe.OPTIONAL_HEADER.ImageBase
        secs = []
        for s in pe.sections:
            name = s.Name.rstrip(b"\0").decode("ascii", errors="replace")
            va = s.VirtualAddress
            vsize = max(s.Misc_VirtualSize, s.SizeOfRawData)
            raw_end = va + s.SizeOfRawData
            secs.append({"name": name, "va": va, "end": va + vsize,
                         "raw_end": raw_end})
    finally:
        pe.close()
    return image_base, secs


def section_of(addr, image_base, secs):
    rva = addr - image_base
    for s in secs:
        if s["va"] <= rva < s["end"]:
            bss = rva >= s["raw_end"]
            return s["name"], bss
    return "none", False


GAP_LABELS = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]


def gap_bucket(gap):
    for t in GAP_LABELS:
        if gap <= t:
            return str(t)
    return ">4096"


def main():
    recs, files_scanned = scan()
    image_base, secs = load_sections()

    addrs = sorted(recs.keys(), key=lambda k: int(k, 16))
    sec_info = {}
    for a in addrs:
        ival = int(a, 16)
        sec_info[a] = section_of(ival, image_base, secs)

    # next-higher DAT in the same section
    next_of = {}
    last_in_sec = {}
    for a in reversed(addrs):
        sec = sec_info[a][0]
        if sec in last_in_sec:
            nxt = last_in_sec[sec]
            next_of[a] = nxt
        last_in_sec[sec] = a

    globals_out = []
    for a in addrs:
        r = recs[a]
        ival = int(a, 16)
        sec, bss = sec_info[a]
        nxt = next_of.get(a)
        gap = (int(nxt, 16) - ival) if nxt else None
        globals_out.append({
            "addr": "0x" + a,
            "decls": r["decls"],
            "defs": r["defs"],
            "declared_types": sorted(r["types"]),
            "n_files": len(r["files"]),
            "n_refs": r["n_refs"],
            "uses_address_of": r["uses_address_of"],
            "section": sec,
            "bss": bss,
            "next_addr": ("0x" + nxt) if nxt else None,
            "gap": gap,
        })

    os.makedirs(OUT_DIR, exist_ok=True)
    meta = {
        "reference_image": REF_IMAGE,
        "image_base": "0x%08x" % image_base,
        "sections": [{"name": s["name"], "va": "0x%08x" % (image_base + s["va"]),
                      "end": "0x%08x" % (image_base + s["end"]),
                      "raw_end": "0x%08x" % (image_base + s["raw_end"])}
                     for s in secs],
        "input_roots": INPUT_ROOTS,
        "files_scanned": files_scanned,
        "distinct_addresses": len(globals_out),
        "total_refs": sum(g["n_refs"] for g in globals_out),
    }
    json_path = os.path.join(OUT_DIR, "dat_globals.json")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "globals": globals_out}, fh, indent=1)

    # ---- summary ----
    lines = []
    lines.append("DAT_ global inventory")
    lines.append("reference image: %s (image base 0x%08x)" % (REF_IMAGE, image_base))
    lines.append("files scanned: %d" % files_scanned)
    lines.append("distinct DAT_ addresses: %d" % len(globals_out))
    lines.append("total references: %d" % meta["total_refs"])
    lines.append("")
    sec_cnt = Counter(g["section"] for g in globals_out)
    lines.append("By section:")
    for name, c in sorted(sec_cnt.items(), key=lambda kv: -kv[1]):
        lines.append("  %-10s %d" % (name, c))
    bss_cnt = Counter(g["bss"] for g in globals_out)
    lines.append("By bss flag (uninitialised tail): true=%d false=%d" %
                 (bss_cnt.get(True, 0), bss_cnt.get(False, 0)))
    lines.append("")
    ntypes = Counter(min(len(g["declared_types"]), 2) for g in globals_out)
    lines.append("Distinct declared types: 0=%d 1=%d >1=%d" %
                 (ntypes.get(0, 0), ntypes.get(1, 0), ntypes.get(2, 0)))
    with_defs = sum(1 for g in globals_out if g["defs"])
    lines.append("With file-scope definitions (non-extern): %d" % with_defs)
    lines.append("")
    lines.append("Top 20 most referenced:")
    top = sorted(globals_out, key=lambda g: (-g["n_refs"], g["addr"]))[:20]
    for g in top:
        lines.append("  %s refs=%d files=%d section=%s type=%s" % (
            g["addr"], g["n_refs"], g["n_files"], g["section"],
            ",".join(g["declared_types"]) or "-"))
    lines.append("")
    lines.append("Gap to next DAT in same section (bucket = smallest threshold >= gap):")
    gcnt = Counter()
    no_next = 0
    for g in globals_out:
        if g["gap"] is None:
            no_next += 1
        else:
            gcnt[gap_bucket(g["gap"])] += 1
    for t in [str(x) for x in GAP_LABELS] + [">4096"]:
        lab = t if t.startswith(">") else "<= " + t
        lines.append("  %-8s %d" % (lab, gcnt.get(t, 0)))
    lines.append("  no next in section: %d" % no_next)
    lines.append("")
    summary_path = os.path.join(OUT_DIR, "dat_globals_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("\n".join(lines))
    print("\nWrote:", json_path)
    print("Wrote:", summary_path)


if __name__ == "__main__":
    main()
