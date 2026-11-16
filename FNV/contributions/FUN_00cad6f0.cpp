struct FUN_00cad6f0_class
{
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c; int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68; int unk6c; int unk70; int unk74; int unk78; int unk7c;
    void** items;
    volatile int itemCount;
    void __thiscall FUN_00cad6f0(void* item);
};
void FUN_00cad6f0_class::FUN_00cad6f0(void* item)
{
    int index = 0;
    int count = itemCount;
    if (count <= 0)
        goto notFound;
    void** entry = items;
    do
    {
        if (*entry == item)
            goto found;
        ++index;
        ++entry;
    } while (index < count);
notFound:
    index = -1;
found:
    --itemCount;
    int newCount = itemCount;
    if (newCount != index)
    {
        void** entry2 = items;
        entry2[index] = entry2[newCount];
    }
}




