struct hkReferencedObject {
    void removeReference();
};
struct Item : hkReferencedObject {
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
    void FUN_00d07c80(void* owner);
};
struct Manager { void FUN_00c95800(Item** entries, int count); };
struct Collection { virtual void slot00(); virtual void removeItems(Manager* manager); };
struct AllocatorOwner {
    int unk00; int unk04; Collection collection; int unk0C; int unk10; Manager* manager; Item* entries[6];
    void FUN_00d0b570();
};
void AllocatorOwner::FUN_00d0b570() {
    if (manager == 0) return;
    manager->FUN_00c95800(entries, 6);
    Item** current = entries;
    void* owner = &unk0C;
    int count = 6;
    do {
        (*current)->FUN_00d07c80(owner);
        (*current)->removeReference();
        *current = 0;
        ++current;
        --count;
    } while (count != 0);
    collection.removeItems(manager);
    manager = 0;
}

