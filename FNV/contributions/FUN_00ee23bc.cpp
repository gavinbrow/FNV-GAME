extern "C" double __cdecl FUN_00ee23bc(double v)
{
    double r;
    __asm {
        fld v
        frndint
        fstp r
    }
    return r;
}
