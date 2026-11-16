struct OldReference { ~OldReference(); };
struct ExtraReference : BSExtraData {
    OldReference* reference;
    ExtraReference(OldReference* value);
    void FUN_004f15a0(unsigned int extraType);
};
struct FUN_00418f60_shell : ExtraDataList {
    ExtraReference* FUN_00418f60(OldReference* replacement);
};
ExtraReference* FUN_00418f60_shell::FUN_00418f60(OldReference* replacement)
{
    ExtraReference* extra = static_cast<ExtraReference*>(GetExtraData(0x40));
    if (extra != 0) {
        delete extra->reference;
        extra->reference = replacement;
        return extra;
    }
    extra = new ExtraReference(replacement);
    extra->FUN_004f15a0(0x40);
    AddExtra(extra);
    return extra;
}