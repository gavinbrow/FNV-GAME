struct ItemFlags {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int flags;
};
struct ItemEntry {
    unsigned int unk00;
    unsigned int unk04;
    ItemFlags* details;
};
struct CountProvider {
    virtual void unused();
    virtual unsigned int LastIndex();
};
struct ItemContainer {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    CountProvider counter;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    ItemEntry** entries;
};
struct ItemCollection {
    unsigned int unk00;
    unsigned int unk04;
    ItemContainer* container;
    unsigned int unk0c;
    unsigned int defaultFlags;
    unsigned int __thiscall FUN_00ccfb40(unsigned int index);
};
unsigned int ItemCollection::FUN_00ccfb40(unsigned int index) {
    if (index != 0xffffffffu) {
        unsigned int lastIndex;
        if (this != 0) {
            ItemContainer* current = container;
            if (current != 0)
                lastIndex = current->counter.LastIndex();
            else
                lastIndex = 0;
        } else
            lastIndex = 0;
        if (index <= lastIndex && this != 0 && container != 0) {
            ItemEntry* entry = container->entries[index];
            if (entry != 0 && entry->details != 0)
                return entry->details->flags & 0x1f;
        }
    }
    return defaultFlags & 0x1f;
}