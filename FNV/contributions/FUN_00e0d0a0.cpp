struct Entry { void __thiscall FUN_00ddeff0(unsigned int flags); };
struct Device {
    virtual void A();
    virtual void B();
    virtual void C();
    virtual void D();
    virtual void ReleaseBuffer(void* p, unsigned int bytes);
};
void* __cdecl FUN_00c85750();
struct Owner {
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14;
    int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c;
    Entry** items;
    int count;
    unsigned int flags;
    void FUN_00e0d0a0();
};
void Owner::FUN_00e0d0a0() {
    int index = 0;
    int zero = 0;
    if (count > 0) {
        do {
            Entry* entry = items[index];
            if (entry != 0)
                entry->FUN_00ddeff0(1);
            ++index;
        } while (index < count);
    }
    count = zero;
    void* holder = FUN_00c85750();
    Device* device = *(Device**)((char*)holder + 0x10);
    unsigned int mask = 0x80000000;
    unsigned int value = flags;
    count = zero;
    if ((mask & value) == 0) {
        unsigned int bytes = (value & 0x3fffffff) * 4;
        device->ReleaseBuffer(items, bytes);
    }
    flags = mask;
    items = 0;
}
