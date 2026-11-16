"""Build the exe on this PC and upload it as a new private GitHub release.

Run:  python tools/publish_release.py [--no-harness] [--notes "text"]

Steps: export the live tree into this repo -> commit + push if anything changed -> build-all.cmd from the live
tree into dist/ -> zip (exe, README, setup script, summaries) -> `gh release create build-N`.
No game files or Steam files ever go in the zip: setup_play.cmd links/copies them from the player's own install.
"""
import argparse, glob, os, re, subprocess, sys, zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.environ.get("FNV_PROJ_ROOT", os.path.dirname(REPO))
GH_REPO = "gavinbrow/FNV-GAME"


def run(cmd, **kw):
    print(">", " ".join(cmd) if isinstance(cmd, list) else cmd, flush=True)
    return subprocess.run(cmd, check=True, **kw)


def out(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout.strip()


def next_tag():
    tags = out(["gh", "release", "list", "-R", GH_REPO, "--limit", "200", "--json", "tagName",
                "--jq", ".[].tagName"]).split()
    nums = [int(m.group(1)) for t in tags if (m := re.fullmatch(r"build-(\d+)", t))]
    return f"build-{max(nums, default=0) + 1}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-harness", action="store_true")
    ap.add_argument("--notes", default="")
    ap.add_argument("--use-dist", action="store_true", help="publish the exe already in dist/ (built and tested) without rebuilding")
    a = ap.parse_args()

    run([sys.executable, os.path.join(REPO, "tools", "export_repo.py")])
    run(["git", "-C", REPO, "add", "-A"])
    if subprocess.run(["git", "-C", REPO, "diff", "--cached", "--quiet"]).returncode:
        run(["git", "-C", REPO, "commit", "-q", "-m", "Sync source and build scripts"])
    run(["git", "-C", REPO, "push", "-q", "origin", "main"])
    sha = out(["git", "-C", REPO, "rev-parse", "HEAD"])

    dist = os.path.join(REPO, "dist")
    build = [os.path.join(PROJ, "runtime-next", "build-all.cmd"), "--out", dist]
    build.append("--no-harness" if a.no_harness else "--require-harness")   # a failed game test stops the release
    if not a.use_dist:
        run(["cmd", "/c"] + build)
    exe = os.path.join(dist, "FalloutNV_selfbuilt.exe")
    if not os.path.isfile(exe):
        sys.exit("build produced no exe")

    tag = next_tag()
    zpath = os.path.join(dist, f"FNV-selfbuilt-{tag}.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(exe, "FalloutNV_selfbuilt.exe")
        z.write(os.path.join(REPO, "README-PLAY.md"), "README.txt")
        z.write(os.path.join(REPO, "tools", "setup_play.cmd"), "setup_play.cmd")
        for f in ("build-summary.txt", "build-summary.json", "harness-verdict.json"):
            p = os.path.join(dist, f)
            if os.path.isfile(p):
                z.write(p, f)

    notes_file = os.path.join(dist, "build-summary.txt")
    notes = (a.notes + "\n\n" if a.notes else "") + (open(notes_file, encoding="utf-8").read()
                                                     if os.path.isfile(notes_file) else "")
    run(["gh", "release", "create", tag, zpath, "-R", GH_REPO, "--title", f"Self-built {tag}",
         "--notes", notes or f"Self-compiled build from {sha}.", "--target", sha])
    print(f"published {tag}")


if __name__ == "__main__":
    main()
