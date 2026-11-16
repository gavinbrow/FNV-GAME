struct FNVCommandResult {
    int __thiscall FUN_005a6150();
    int __thiscall FUN_005def70();
};
extern void __cdecl FUN_005accb0(int a1, int a2, int a8, int a3, int a4, int a5, int a6, FNVCommandResult** out);
bool __cdecl FUN_005deef0(int a1, int a2, int a3, int a4, int a5, int a6, double* output, int a8) {
    int v;
    FNVCommandResult* p = 0;
    FUN_005accb0(a1, a2, a8, a3, a4, a5, a6, &p);
    if (p != 0) {
        if (!p->FUN_005a6150() && !p->FUN_005def70()) {
            v = 0;
        } else {
            v = 1;
        }
        *output = static_cast<double>(v);
    } else {
        return false;
    }
    return true;
}