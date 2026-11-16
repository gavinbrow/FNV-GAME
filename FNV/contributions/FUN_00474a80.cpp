extern char DAT_01183028;
extern char DAT_011840c4;
extern int __cdecl FUN_00ec43fb(int target, int zero, const char* first, const char* second, int finalValue);
struct RangeHolder {
    int* FUN_006815c0();
};
struct GroupHolder {
    RangeHolder* FUN_00500940();
};
struct FUN_00474a80_Class {
    GroupHolder* FUN_00474a40();
    bool FUN_00474a80();
};
bool FUN_00474a80_Class::FUN_00474a80()
{
    if (FUN_00474a40()) {
        int value = *FUN_00474a40()->FUN_00500940()->FUN_006815c0();
        if (value != 0) {
            int result = FUN_00ec43fb(value, 0, &DAT_01183028, &DAT_011840c4, 0);
            if (result == 0)
                return true;
        }
    }
    return false;
}