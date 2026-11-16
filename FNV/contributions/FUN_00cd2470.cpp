struct AllocatorState
{
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    void* allocator;
};
extern AllocatorState* __cdecl FUN_00c85750();
extern void __cdecl FUN_00c90940(void* allocator, void* array, int elementSize);
struct PointerArray
{
    void** data;
    int count;
    int capacity;
};
struct Candidate
{
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    int unk28;
    int unk2C;
    int unk30;
    int unk34;
    int unk38;
    int unk3C;
    int unk40;
    int unk44;
    int unk48;
    int unk4C;
    int unk50;
    int unk54;
    int unk58;
    int unk5C;
    int unk60;
    int unk64;
    int unk68;
    int unk6C;
    int unk70;
    int unk74;
    int unk78;
    int unk7C;
    int unk80;
    PointerArray items;
    void* FUN_00cd2470(void* value);
};
void* Candidate::FUN_00cd2470(void* value)
{
    PointerArray* array = &items;
    register int index = 0;
    int count = array->count;
    if (count > 0)
    {
        void** entry = array->data;
        do
        {
            if (*entry == value)
                goto found;
            ++index;
            ++entry;
        } while (index < count);
    }
    goto append;
found:
    if (index >= 0)
        return (void*)index;
append:
    AllocatorState* state = FUN_00c85750();
    if (array->count == (array->capacity & 0x3fffffff))
        FUN_00c90940(state->allocator, array, 4);
    void** slot = array->data + array->count;
    *slot = value;
    ++array->count;
    return slot;
}


