struct CommandResult {
    int __thiscall FUN_005a60d0();
};
extern void __cdecl FUN_005accb0(int arg1, int arg2, int arg8,
                                  int arg3, int arg4, int arg5,
                                  int arg6, CommandResult** result);

bool __cdecl FUN_005dee90(int arg1, int arg2, int arg3, int arg4,
                          int arg5, int arg6, double* output, int arg8)
{
    CommandResult* status = 0;
    FUN_005accb0(arg1, arg2, arg8, arg3, arg4, arg5, arg6, &status);
    if (status) {
        int value = status->FUN_005a60d0();
        *output = static_cast<double>(value);
    } else {
        return false;
    }
    return true;
}