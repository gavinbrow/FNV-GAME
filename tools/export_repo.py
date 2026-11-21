"""Copy the buildable source and scripts from the live work tree into this repo.

Run:  python tools/export_repo.py [--dry-run]

Copies:
  fnv_decomp/   every file git tracks or would track there (its .gitignore applies), minus backups
  runtime-next/ scripts and notes (*.py *.cmd *.md *.txt), plus small *.json specs (<= 4 MB)
  extra files listed in tools/export_extra.txt (one path per line, relative to the project root)

Never copies game files, executables, objects, libraries, run folders, harness output or backups.
"""
import os, re, shutil, subprocess, sys, fnmatch
from pathlib import Path

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.environ.get("FNV_PROJ_ROOT", os.path.dirname(HERE))
DRY = "--dry-run" in sys.argv

BAN_EXT = {".exe", ".dll", ".obj", ".lib", ".pdb", ".ilk", ".map", ".bsa", ".esm", ".esp", ".esp",
           ".bik", ".zip", ".7z", ".iso", ".res", ".bin", ".dmp", ".png", ".jpg", ".bmp", ".dds", ".log"}
BAN_DIR = {"run", "harness-out", "backup", "__pycache__", "out", "logs", "tmp", "scratch", ".git"}
BAN_GLOB = ["*.bak*", "*.bak", "prev-*", "obj_v*", "ehvar", "*.orig", "*.tmp",
            "*.before-*", "promotion-staged*"]
# Not shipped: superseded stages, one-off debug/experiment scripts, scratch notes, stale result dumps.
# Everything here was checked against what runtime-next/build_all.py (build-all.cmd) actually runs, directly or
# through imports and data files it names; nothing under BAN_PREFIX / BAN_FILES is needed by the build.
# Paths are relative to the project root, forward slashes. KEEP wins over BAN_PREFIX.
BAN_PREFIX = [
    "runtime-next/build-v4/",       # first assembler generation, superseded by build-v7
    "runtime-next/build-v6/",       # second assembler generation, superseded by build-v7
    "runtime-next/build-v7/w2-tools/",  # worker-2 debug helpers (dbg, try1, var1, var2, fndiff, ...)
    "runtime-next/contrib-v5/",     # old contribution assembler, superseded
    "runtime-next/layout-v1/",      # first layout experiments, superseded by layout-v2
    "runtime-next/link-triage/",    # one-off link triage
    "runtime-next/link-v2/",        # abandoned real-linker experiment (dbg*, mk*, link1.cmd, ...)
    "runtime-next/overlay-test/",   # live process overlay experiments
    "runtime-next/data-v2/",        # data placement experiments (rename_*, pilot_*, batch_*); build keeps libsecs.py
    "runtime-next/coverage-v3/",    # coverage measurement scripts; build keeps build_extra.py + its outputs
    "runtime-next/reloc-v5/",       # relocation prototype; build keeps what build-v7 imports/reads
    "runtime-next/layout-v2/ci/dist_live/",  # copy of an old build summary
    "runtime-next/layout-v2/build/",  # generated image reports, not source inputs
    "runtime-next/m3/gen/",         # M3 generated sources/objects, rebuilt by the m3-gen build step
]
KEEP = {
    "runtime-next/data-v2/libsecs.py",
    "runtime-next/link-v2/crt_defaddr.json", "runtime-next/link-v2/crt_place.json", "runtime-next/link-v2/extra_labels.json",
    "runtime-next/coverage-v3/build_extra.py", "runtime-next/coverage-v3/extra_pieces.json", "runtime-next/coverage-v3/build_summary.json",
    "runtime-next/reloc-v5/assemble_v5.py", "runtime-next/reloc-v5/crt5.py", "runtime-next/reloc-v5/callee_fixups.json",
    "runtime-next/reloc-v5/progress_v5_raw.json", "runtime-next/reloc-v5/rebase_remaining_v5.json",
    "runtime-next/reloc-v5/tail_alias_candidates.json", "runtime-next/reloc-v5/NOTES.md",
}
BAN_FILES = set("""
runtime-next/PLAN-PLAYABLE.md
runtime-next/build-v7/progress_phase1.json
runtime-next/build-v7/contrib_pieces.json
runtime-next/layout-v2/snapshot/contrib_pieces.json
runtime-next/direct-v1/d86.py
runtime-next/direct-v1/dbg.py
runtime-next/direct-v1/drive.py
runtime-next/direct-v1/launch.ps1
runtime-next/direct-v1/libimps.py
runtime-next/direct-v1/make_direct.py
runtime-next/direct-v1/rebase_exe.py
runtime-next/direct-v1/scan_imps.py
runtime-next/direct-v1/validate_imports.py
runtime-next/direct-v1/objs_imps.json
runtime-next/layout-v2/dis_img.py
runtime-next/layout-v2/newtoold.py
runtime-next/layout-v2/ci/sync_clone.cmd
runtime-next/layout-v2/ci/scan_deps.py
runtime-next/layout-v2/ci/scan_deps.json
runtime-next/layout-v2/ci/relocate_paths.py
runtime-next/layout-v2/build/image_REV.json
runtime-next/layout-v2/build/image_U.json
runtime-next/layout-v2/build/image_Z.json
runtime-next/layout-v2/build/last_G.json
runtime-next/layout-v2/build/last_REV.json
runtime-next/layout-v2/build/last_U.json
runtime-next/layout-v2/build/last_Z.json
runtime-next/pinned-build/check_units_v3.py
runtime-next/pinned-build/diag_tails_v2.py
runtime-next/pinned-build/gate_v3.py
runtime-next/pinned-build/layouts_v3.py
runtime-next/pinned-build/pieces_all_v2.py
runtime-next/pinned-build/recon.py
runtime-next/pinned-build/rev_fix_v3.py
runtime-next/pinned-build/tail_fix_v3.py
runtime-next/pinned-build/uncovered_bytes_v2.py
runtime-next/reloc-v7/breakdown.py
runtime-next/reloc-v7/breakdown_report.py
runtime-next/reloc-v7/breakdown_baseline.md
runtime-next/reloc-v7/breakdown_fields.json
runtime-next/reloc-v7/changed_files.txt
runtime-next/reloc-v7/cmp_strict.py
runtime-next/reloc-v7/derive_new.py
runtime-next/reloc-v7/edits2.py
runtime-next/reloc-v7/edited_units_all.json
runtime-next/reloc-v7/edited_units_b2.json
runtime-next/reloc-v7/edited_units_consts.json
runtime-next/reloc-v7/emit2asm.py
runtime-next/reloc-v7/find_units.py
runtime-next/reloc-v7/fix2.py
runtime-next/reloc-v7/fix_consts.py
runtime-next/reloc-v7/funclets_integrated.json
runtime-next/reloc-v7/gaps2asm.py
runtime-next/reloc-v7/inf_apply.py
runtime-next/reloc-v7/inf_list.py
runtime-next/reloc-v7/inf_list.json
runtime-next/reloc-v7/inf_touched.json
runtime-next/reloc-v7/inf_units.json
runtime-next/reloc-v7/integrate_funclets.py
runtime-next/reloc-v7/integrate_gaps.py
runtime-next/reloc-v7/lstsyms.py
runtime-next/reloc-v7/merge_fix.py
runtime-next/reloc-v7/mk_overlay.py
runtime-next/reloc-v7/one.json
runtime-next/reloc-v7/rb.cmd
runtime-next/reloc-v7/rebase_base.json
runtime-next/reloc-v7/recompile_units.py
runtime-next/reloc-v7/sidecar_update.py
runtime-next/reloc-v7/summ.py
runtime-next/reloc-v7/t_db.py
runtime-next/reloc-v7/e2a_all/report.json
runtime-next/reloc-v7/e2a_test/report.json
runtime-next/reloc-v7/gaps_out/good.json
runtime-next/reloc-v7/gaps_out/report.json
fnv_decomp/AGENTS.md
fnv_decomp/docs/rebuild/AGENT-WORK.md
runtime-next/m3/phase2/MCP-CONNECTION-20261119.md
runtime-next/m3/phase2/PAUSED-NON-AI-20261120.md
""".split())
BAN_GLOB_PATH = ["fnv_decomp/docs/rebuild/CLAUDE-*-HANDOFF.md"]   # AI hand-off notes

# Personal paths are rewritten while copying (the build only uses them as defaults that env vars override).
SCRUB_EXT = {".py", ".cmd", ".md", ".txt", ".ps1", ".bat", ".json"}
_NAMES = {os.environ.get("USERNAME"), os.environ.get("USER"), os.path.basename(os.path.expanduser("~"))} - {None, "", "Public", "Default"}
_ME = b"(?:" + b"|".join(re.escape(x.encode()) for x in sorted(_NAMES) or ["nobody-user"]) + b")"
SCRUB = [
    # the per-user site-packages default keeps working for whoever clones the repo (they still override it with FNV_PY_SITE)
    (re.compile(rb"(?i)r'C:\\Users\\" + _ME + rb"\\AppData\\Roaming\\([^']*)'"), rb"__import__('os').path.expandvars(r'%APPDATA%\\\1')"),
    (re.compile(rb"(?i)J\('C:' \+ chr\(92\), 'Users', '" + _ME + rb"', 'AppData', 'Roaming', "), rb"J(os.environ.get('APPDATA', ''), "),
    (re.compile(rb"(?i)(Users[\\/]+)" + _ME + rb"(?![A-Za-z0-9_])"), rb"\1<user>"),
    (re.compile(rb"(?i)('Users',\s*)'" + _ME + rb"'"), rb"\1'<user>'"),
    # Preserve slash escaping in JSON and Python literals while removing the
    # author's workspace location. FNV_PROJ_ROOT selects the real checkout.
    (re.compile(rb"(?i)C:([\\/]+)Projects[\\/]+Decompilation"),
     lambda m: b"C:" + m[1] + b"path" + m[1] + b"to" + m[1] + b"Decompilation"),
]


def scrubbed(src):
    """Bytes of src with the current user's name removed from paths, or None when src is not scrubbed or is clean."""
    if os.path.splitext(src)[1].lower() not in SCRUB_EXT:
        return None
    data = Path(src).read_bytes()
    out = data
    for rx, rep in SCRUB:
        out = rx.sub(rep, out)
    return out if out != data else None

RT_EXT = {".py", ".cmd", ".md", ".txt", ".ps1", ".bat"}
RT_JSON_MAX = 4 * 1024 * 1024


def banned(rel):
    r = rel.replace("\\", "/")
    if r not in KEEP:
        if r in BAN_FILES or any(r.startswith(p) for p in BAN_PREFIX) or any(fnmatch.fnmatch(r, g) for g in BAN_GLOB_PATH):
            return True
    parts = r.split("/")
    for p in parts:
        if p in BAN_DIR or any(fnmatch.fnmatch(p, g) for g in BAN_GLOB):
            return True
    return os.path.splitext(rel)[1].lower() in BAN_EXT


def fnv_decomp_files():
    root = os.path.join(PROJ, "fnv_decomp")
    out = subprocess.run(["git", "-C", root, "ls-files", "-co", "--exclude-standard", "-z"],
                         capture_output=True, check=True).stdout.decode("utf-8").split("\0")
    for rel in out:
        if rel and not banned("fnv_decomp/" + rel) and not rel.startswith(".github/"):
            yield os.path.join("fnv_decomp", rel)


def runtime_files():
    root = os.path.join(PROJ, "runtime-next")
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if not banned(d)]
        for fn in fns:
            full = os.path.join(dp, fn)
            rel = os.path.relpath(full, PROJ)
            if banned(rel):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext in RT_EXT or (ext == ".json" and os.path.getsize(full) <= RT_JSON_MAX):
                yield rel


def extra_files():
    lst = os.path.join(HERE, "tools", "export_extra.txt")
    if os.path.exists(lst):
        for line in open(lst, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and not banned(line):
                yield line


def main():
    n = size = scrubbed_n = 0
    keep = set()
    for rel in list(fnv_decomp_files()) + list(runtime_files()) + list(extra_files()):
        src = os.path.join(PROJ, rel)
        if not os.path.isfile(src):
            continue
        dst = os.path.join(HERE, rel)
        n += 1
        size += os.path.getsize(src)
        keep.add(os.path.normcase(dst))
        clean = scrubbed(src)
        if DRY:
            scrubbed_n += clean is not None
            continue
        if clean is not None:
            if not (os.path.exists(dst) and Path(dst).read_bytes() == clean):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                Path(dst).write_bytes(clean)
                shutil.copystat(src, dst)
            scrubbed_n += 1
            continue
        if os.path.exists(dst) and Path(dst).read_bytes() == Path(src).read_bytes():
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    # remove files an earlier export left behind that are now banned or gone from the live tree
    pruned = 0
    for top in ("fnv_decomp", "runtime-next", "FNV"):
        for dp, dns, fns in os.walk(os.path.join(HERE, top)):
            for fn in fns:
                full = os.path.join(dp, fn)
                if os.path.normcase(full) not in keep:
                    pruned += 1
                    if not DRY:
                        os.remove(full)
        if not DRY:
            for dp, dns, fns in os.walk(os.path.join(HERE, top), topdown=False):
                if not os.listdir(dp):
                    os.rmdir(dp)
    print(f"{n} files, {size / 1e6:.1f} MB{' (dry run)' if DRY else ''}; {scrubbed_n} scrubbed, {pruned} stale removed")


if __name__ == "__main__":
    main()
