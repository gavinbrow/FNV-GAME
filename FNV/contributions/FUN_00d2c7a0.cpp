struct FUN_00d2c7a0_Slot {
    void* object;
    int unk04;
};

struct FUN_00d2c7a0_class {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00d2c7a0_Slot slots[17];
    void __thiscall FUN_00d2c520(int index);
    void __thiscall FUN_00d2c7a0();
};

void FUN_00d2c7a0_class::FUN_00d2c7a0()
{
    int index = 16;
    FUN_00d2c7a0_Slot* slot = slots + 16;
    while (index >= 0) {
        if (slot->object)
            FUN_00d2c520(index);
        --index;
        --slot;
    }
}
