# Credits

## Decompiled source: fnv_decomp

The decompiled C++ source in [`fnv_decomp/`](fnv_decomp/) comes from the
**[momusdigital/fnv_decomp](https://github.com/momusdigital/fnv_decomp)** project, coordinated on
[fnvdecomp.com](https://fnvdecomp.com). Its community of contributors rebuilt the game function by function, and
every one of those matched functions is what this repository compiles into the self-built executable.

The named contributors and their matched functions are listed in
[fnv_decomp/CREDITS.md](fnv_decomp/CREDITS.md); 8 further contributors took part anonymously. Thank you to all of
them.

The fnv_decomp licence ([fnv_decomp/LICENSE](fnv_decomp/LICENSE)) applies to that source: no licence is granted,
and the contributors keep the rights to their own contributions.

## Function names

Most readable function names in the name map (`fnv_decomp/tools/function_names_data.py`, documented in
[fnv_decomp/docs/function-names.md](fnv_decomp/docs/function-names.md)) come from
[fnv_decomp pull request 42](https://github.com/momusdigital/fnv_decomp/pull/42) by mathisto, which links PC
functions to the original names in two Xbox 360 development builds. Only its high-confidence links are used.

## This repository

The build pipeline in `runtime-next/` (compiling, laying out code and data, assembling and testing the executable),
the play setup and the release tooling in `tools/` were built on top of fnv_decomp for this repository.

Original contributions owned by gavinbrow, including original source and
header changes in any directory, tooling and documentation, are available
under the [MIT licence](LICENSE), within the scope stated there. Contributions
from others are covered only when their copyright holders expressly choose
these terms. Free use, modification and redistribution require keeping the
copyright and permission notices as attribution.
Please retain this credits file when sharing the project so the upstream
contributors remain acknowledged. Upstream work and original game materials
keep their existing terms. Licensing an original addition does not grant
permission to reuse the pre-existing material in a mixed file.

## Third-party code

- zlib 1.2.1 by Jean-loup Gailly and Mark Adler, under its own licence
  ([fnv_decomp/third_party/zlib-1.2.1](fnv_decomp/third_party/zlib-1.2.1)).

## The game

*Fallout: New Vegas* is the work of Obsidian Entertainment and Bethesda Softworks. *Fallout* and related names are
trademarks of their respective owners. This project is not affiliated with or endorsed by them.
