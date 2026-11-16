// FUN_00ee6daa — import forwarding stub: a tail jump through the ws2_32
// import table slot to ntohs. The wrapper's own argument is already in the
// callee's argument position, so with matching __stdcall cleanup the /O2
// tail call compiles to a single `jmp dword ptr [__imp__ntohs@4]` (6 bytes).
//
// Target: size 6, /MT /O2 /GS /EHsc /Gy.

__declspec(dllimport) unsigned short __stdcall ntohs(unsigned short netshort);

unsigned short __stdcall FUN_00ee6daa(unsigned short netshort)
{
    return ntohs(netshort);
}
