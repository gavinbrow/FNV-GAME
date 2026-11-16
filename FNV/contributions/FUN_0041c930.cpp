struct Package_0041c930 {
    bool FUN_00674d40();
    int FUN_0041ca90();
    bool FUN_00674e40();
};
struct Extra_00432870 : public BSExtraData {
    Package_0041c930* pPackage;
    unsigned int packageArgument;
    unsigned int packageOptions;
    unsigned char flag1;
    unsigned char flag2;
    unsigned char flag3;
    unsigned char pad1B;
    Extra_00432870(Package_0041c930*, unsigned int, unsigned int, unsigned char, unsigned char, unsigned char);
};
struct FUN_0041c930_shell : public ExtraDataList {
    void FUN_0041cc60();
    void FUN_0041c930(Package_0041c930*, unsigned int, unsigned int, unsigned char, unsigned char, unsigned char);
};
void FUN_0041c930_shell::FUN_0041c930(Package_0041c930* package, unsigned int value, unsigned int options, unsigned char flag1, unsigned char flag2, unsigned char flag3)
{
    if (package != 0 &&
        ((package->FUN_00674d40() && package->FUN_0041ca90() != 1) ||
         package->FUN_00674e40() ||
         package->FUN_0041ca90() == 0x18 ||
         package->FUN_0041ca90() == 0x17)) {
        return;
    }
    Extra_00432870* extra = static_cast<Extra_00432870*>(GetExtraData(0x19));
    if (package != 0) {
        if (extra == 0) {
            extra = new Extra_00432870(package, value, options, flag1, flag2, flag3);
            AddExtra(extra);
        } else {
            extra->pPackage = package;
            extra->packageArgument = value;
            extra->packageOptions = options;
            extra->flag1 = flag1;
            extra->flag2 = flag2;
            extra->flag3 = flag3;
        }
    } else if (extra != 0) {
        FUN_0041cc60();
    }
}