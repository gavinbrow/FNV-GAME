"""Copy the buildable source and scripts from the live work tree into this repo.

Run:  python tools/export_repo.py [--dry-run]

Copies:
  fnv_decomp/   every file git tracks or would track there (its .gitignore applies), minus backups
  runtime-next/ scripts and notes (*.py *.cmd *.md *.txt), plus small *.json specs (<= 4 MB)
  extra files listed in tools/export_extra.txt (one path per line, relative to the project root)

Never copies game files, executables, objects, libraries, run folders, harness output or backups.
"""
import os, shutil, subprocess, sys, fnmatch

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.environ.get("FNV_PROJ_ROOT", os.path.dirname(HERE))
DRY = "--dry-run" in sys.argv

BAN_EXT = {".exe", ".dll", ".obj", ".lib", ".pdb", ".ilk", ".map", ".bsa", ".esm", ".esp", ".esp",
           ".bik", ".zip", ".7z", ".iso", ".res", ".bin", ".dmp", ".png", ".jpg", ".bmp", ".dds", ".log"}
BAN_DIR = {"run", "harness-out", "backup", "__pycache__", "out", "logs", "tmp", "scratch", ".git"}
BAN_GLOB = ["*.bak*", "*.bak", "prev-*", "obj_v*", "ehvar", "*.orig", "*.tmp"]
RT_EXT = {".py", ".cmd", ".md", ".txt", ".ps1", ".bat"}
RT_JSON_MAX = 4 * 1024 * 1024


def banned(rel):
    parts = rel.replace("\\", "/").split("/")
    for p in parts:
        if p in BAN_DIR or any(fnmatch.fnmatch(p, g) for g in BAN_GLOB):
            return True
    return os.path.splitext(rel)[1].lower() in BAN_EXT


def fnv_decomp_files():
    root = os.path.join(PROJ, "fnv_decomp")
    out = subprocess.run(["git", "-C", root, "ls-files", "-co", "--exclude-standard", "-z"],
                         capture_output=True, check=True).stdout.decode("utf-8").split("\0")
    for rel in out:
        if rel and not banned(rel) and not rel.startswith(".github/"):
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
    n = size = 0
    for rel in list(fnv_decomp_files()) + list(runtime_files()) + list(extra_files()):
        src = os.path.join(PROJ, rel)
        if not os.path.isfile(src):
            continue
        dst = os.path.join(HERE, rel)
        n += 1
        size += os.path.getsize(src)
        if DRY:
            continue
        if os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src) and \
                os.path.getmtime(dst) >= os.path.getmtime(src):
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    print(f"{n} files, {size / 1e6:.1f} MB{' (dry run)' if DRY else ''}")


if __name__ == "__main__":
    main()
