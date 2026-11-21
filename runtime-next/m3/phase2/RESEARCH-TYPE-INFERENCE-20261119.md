# Additional non-AI type inference: bounded source review

Date: 2026-11-19. Coordinator research; no installations, binary analysis,
compiler invocations, source integration or queue changes.

## Useful additional lead: BTIGhidra

[Trail of Bits BTIGhidra](https://github.com/trailofbits/BTIGhidra) is a static,
interprocedural type inference extension. It propagates type constraints across
function calls and can accept known signatures as seeds. This addresses a real
remaining question: compatible member types may be evident only when several
functions' accesses are considered together. The underlying solver is ordinary
program analysis, not an LLM. The public repository's build instructions reference
Ghidra 11.0.1, Java, Gradle and Rust; compatibility with our actual environment
has not been established.

The project's [demonstration](https://github.com/trailofbits/BTIGhidra/blob/main/DEMO.md)
shows recovery of six linked-list fields from several functions, then refinement
using a supplied function signature. Its output still uses synthetic field/type
names, so structural inference must not be presented as original semantic type
or name recovery. The demo also documents a global-type workaround and an optional
debug-output path assumption involving `/tmp`. Those details matter on Windows.

[The authors' explanation](https://blog.trailofbits.com/2024/02/07/binary-type-inference-in-ghidra/)
describes call-graph-based inference and conservative typing. The practical
application here would be one unresolved member/global family, seeded with
verified signatures, compared against existing source and PC access evidence.
It is not a tool for reproducing all original C++ virtual signatures, destructor
ownership, templates or compiler-generated metadata automatically.

The related [GrammaTech Retypd plugin](https://github.com/GrammaTech/retypd-ghidra-plugin)
extracts high-level P-code constraints, runs a Python solver and applies inferred
types back to Ghidra. Its documented setup references Python 3.8 or a container.
Do not install both solvers merely to broaden the tool list. A single small
benchmark must establish additional useful facts first.

## Lower priority: replacing the entire decompiler

[Avast RetDec](https://github.com/avast/retdec) advertises PE/x86 support, PDB
consumption, static-library identification and C++ hierarchy detection. It also
states that the project is in limited maintenance. Switching the full program to
a different C decompiler is not supported as a cost-saving route for this phase:
we already possess matching function bodies and need reconciled native types and
class-generated records. A second decompilation would add another representation
to reconcile without an established exact VC2008 round-trip benefit.

This assessment refers to the original Avast project. Search also returned newer
forks with broader claims; those claims were not independently validated and do
not establish suitability for this target.

## Decision

Rank evidence routes in this order:

1. Existing local PC RTTI/COFF/source facts and saved passing experiments.
2. Pinned upstream debug mappings and community declarations, corroborated on PC.
3. Context-aware source AST extraction to group compatible declarations.
4. Targeted Ghidra recovery/type inference for a named residual question.
5. Heavier symbolic-recovery or alternative-decompiler setup only after the
   simpler routes fail to supply a specific needed fact.

A PATH availability check found Java and the Docker CLI; it did not find Clang,
clang-cl or llvm-pdbutil on this process's PATH. This is not a complete inventory
of installed software, does not establish Java version or a running Docker
engine, and is not permission to install dependencies. Existing service and
compiler installations were not traversed.

No tool in this review has yet been run against FNV. Additional supported facts,
usable source proposals and accepted production changes must be counted
separately when a benchmark is run.
