struct FUN_005653d0_class {
    bool FUN_005653d0();
};
struct FUN_00421430_class {
    void FUN_00421430();
};
struct FUN_0056a9b0_shell : TESObjectREFR {
    FUN_00421430_class* FUN_005d43c0(FUN_005653d0_class*);
    void FUN_0056a9b0(FUN_005653d0_class*);
};
void FUN_0056a9b0_shell::FUN_0056a9b0(FUN_005653d0_class* target) {
    if (!target || target->FUN_005653d0()) {
        FUN_005d43c0(target)->FUN_00421430();
    }
}