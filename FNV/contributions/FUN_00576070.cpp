struct FUN_00576070_shell {
    bool FUN_00452370();
    void* FUN_007af430();
    bool FUN_00576070();
};
void* __cdecl FUN_00475400(void* object);
bool FUN_00576070_shell::FUN_00576070() {
    bool result = false;
    if (FUN_00452370()) {
        FUN_00576100_Class* item = (FUN_00576100_Class*)FUN_00475400(FUN_007af430());
        if (item != 0) {
            result = item->FUN_00576100();
        }
        if (((FUN_005760e0_class*)this)->FUN_005760e0()) {
            result = !result;
        }
    }
    return result;
}