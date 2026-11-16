bool __cdecl FUN_007a8e60(
    int a1, int a2, int a3, int a4, int a5, int a6, int a7, int a10,
    va_list* args, int enabled, int left, int right, float zero, float x, float y);

bool __cdecl FUN_00703f10(
    int a1, int a2, int a3, int a4, int a5, int a6, int a7,
    float x, float y, int a10, ...)
{
    if (FUN_004b7210() &&
        ((FUN_009373f0_shell*)FUN_004b7210())->FUN_009373f0())
    {
        bool result5;
        va_list args;
        va_start(args, a10);
        result5 = FUN_007a8e60(
            a1, a2, a3, a4, a5, a6, a7, a10,
            &args, 1, -1, -1, 0.0f, x, y);
        va_end(args);
        return result5;
    }
    return false;
}
