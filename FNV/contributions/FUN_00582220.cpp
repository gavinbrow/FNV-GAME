extern int DAT_01183040;
extern int DAT_01186ab0;
FUN_005822a0_cls* __cdecl FUN_00ec43fb(int key, int zero, void* first, void* second, int trailing);
struct FUN_00582220_Class : FUN_005822a0_cls {
    bool __thiscall FUN_00582220(int key);
};
bool FUN_00582220_Class::FUN_00582220(int key) {
    FUN_005822a0_cls* comparison = FUN_00ec43fb(key, 0, &DAT_01183040, &DAT_01186ab0, 0);
    if (!comparison) {
        return true;
    }
    for (unsigned int index = 0; index < 6; ++index) {
        if (FUN_005822a0(index) != comparison->FUN_005822a0(index)) {
            return true;
        }
    }
    return false;
}
