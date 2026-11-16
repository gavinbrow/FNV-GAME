struct TESObjectREFR;
struct RefListNode {
    unsigned char FUN_008256d0();
    TESObjectREFR*** FUN_006815c0();
    RefListNode* FUN_00726070();
    void FUN_0063f7b0();
    void FUN_00905330(TESObjectREFR*** entry);
};
struct FUN_0041ef20_shell : ExtraDataList {
    void FUN_0041ef20(TESObjectREFR* reference);
};
void FUN_0041ef20_shell::FUN_0041ef20(TESObjectREFR* reference)
{
    if (reference) {
        ExtraWaterLightRefs* extra = (ExtraWaterLightRefs*)GetExtraData(0x54);
        if (extra) {
            RefListNode* current = (RefListNode*)&extra->refs;
            RefListNode* previous = 0;
            while (current && !current->FUN_008256d0()) {
                TESObjectREFR** item = *current->FUN_006815c0();
                if (*item == reference) {
                    if (previous) {
                        previous->FUN_00905330(&item);
                    } else {
                        current->FUN_0063f7b0();
                    }
                    delete item;
                    break;
                }
                current = current->FUN_00726070();
            }
            if (((RefListNode*)&extra->refs)->FUN_008256d0())
                ((FUN_00410020_shell*)this)->FUN_00410020(extra, true);
        }
    }
}