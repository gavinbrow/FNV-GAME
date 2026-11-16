// FUN_00d74420 — __cdecl (caller pops its arguments).
//
// Builds a 12-byte context object on the stack, initializes it to
// (0, 0, 0x80000000), runs its setup pass, resets it, then delegates to the
// helper FUN_00d739f0 and stores its result through the caller's out pointer.
// Finally the context's cleanup pass runs and the function returns 0.

struct FUN_00d74420_Context {
    int m_a;   // +0x00
    int m_b;   // +0x04
    int m_c;   // +0x08, initialized to 0x80000000
    void FUN_00d738f0(int value);
    void FUN_00d74a20();
    void FUN_00d74aa0();
};

int FUN_00d739f0(int a1, int a2, FUN_00d74420_Context* ctx, int a3);

int FUN_00d74420(int a1, int a2, int a3, int* out)
{
    FUN_00d74420_Context ctx;
    ctx.m_a = 0;
    ctx.m_b = 0;
    ctx.m_c = 0x80000000;
    ctx.FUN_00d738f0(a1);
    ctx.FUN_00d74a20();
    *out = FUN_00d739f0(a1, a2, &ctx, a3);
    ctx.FUN_00d74aa0();
    return 0;
}
