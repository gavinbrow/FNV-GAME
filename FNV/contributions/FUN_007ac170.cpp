double __cdecl FUN_00408820(float value);
void __cdecl FUN_00706f30(int message);
struct MenuValueReader { float FUN_00a011b0(unsigned int index); };
struct MenuValueWatcher {
    void* vtable;
    int unk04,unk08,unk0c,unk10,unk14,unk18,unk1c,unk20,unk24;
    MenuValueReader* thresholdSource;
    int unk2c,unk30;
    MenuValueReader* valueSource;
    int unk38,unk3c;
    float lastValue;
    void FUN_007ac170();
};
void MenuValueWatcher::FUN_007ac170()
{
    if (FUN_00408820(valueSource->FUN_00a011b0(0xfc4) - lastValue)
            >= thresholdSource->FUN_00a011b0(0x1007)) {
        FUN_00706f30(4);
        lastValue = valueSource->FUN_00a011b0(0xfc4);
    }
}