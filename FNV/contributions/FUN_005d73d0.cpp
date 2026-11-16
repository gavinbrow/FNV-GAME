extern bool __cdecl FUN_005accb0(int a, int b, int extra, int c, int d, int e, int f, int* result);
extern void __cdecl FUN_007062a0(int a, int b, int c, int d);

bool __cdecl FUN_005d73d0(int a1, int a2, int a3, int a4, int a5, int a6, int a7, int a8)
{
    bool success = true;
    int result = 0;
    if (!FUN_005accb0(a1, a2, a8, a3, a4, a5, a6, &result)) {
        success = false;
    } else {
        FUN_007062a0(1, result, 1, 1);
    }
    return success;
}
