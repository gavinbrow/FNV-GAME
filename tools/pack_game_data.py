"""Pack a play folder's game files into zip parts under GitHub's 2 GB release-asset limit.

Run:  python tools/pack_game_data.py <play folder> <output folder>
Writes FNV-gamedata-NN.zip parts (stored, not compressed: the .bsa archives are already compressed).
Part 01 also holds the small files next to the exe (DLLs, INIs, icon). Saves and logs are skipped.
"""
import os, sys, zipfile

LIMIT = 1_900_000_000
TOP_SKIP_EXT = {".exe", ".log", ".mhd", ".txt"}          # the exe ships in each build release
TOP_KEEP = {"steam_appid.txt"}


def main():
    src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    os.makedirs(out, exist_ok=True)
    top = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))
           and (f in TOP_KEEP or os.path.splitext(f)[1].lower() not in TOP_SKIP_EXT)]
    data = []
    for root, _, files in os.walk(os.path.join(src, "Data")):
        for f in files:
            p = os.path.join(root, f)
            data.append((os.path.getsize(p), os.path.relpath(p, src)))
    parts = [[sum(os.path.getsize(os.path.join(src, f)) for f in top), list(top)]]
    for size, rel in sorted(data, reverse=True):              # first-fit decreasing
        for part in parts:
            if part[0] + size <= LIMIT:
                part[0] += size; part[1].append(rel); break
        else:
            parts.append([size, [rel]])
    for i, (size, files) in enumerate(parts, 1):
        name = os.path.join(out, f"FNV-gamedata-{i:02d}.zip")
        with zipfile.ZipFile(name, "w", zipfile.ZIP_STORED, allowZip64=True) as z:
            for rel in sorted(files):
                z.write(os.path.join(src, rel), rel)
        print(f"{name}: {len(files)} files, {size / 1e9:.2f} GB", flush=True)


if __name__ == "__main__":
    main()
