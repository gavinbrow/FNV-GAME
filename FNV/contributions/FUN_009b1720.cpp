struct EntryRecord {
    int category;
    int unk04;
    int result;
};
struct SearchNode {
    EntryRecord** FUN_006815c0();
    SearchNode* FUN_00726070();
    bool FUN_008256d0();
};
struct MobileObjectBase {
    virtual ~MobileObjectBase();
    unsigned int unk04, unk08, unk0C, unk10, unk14, unk18, unk1C;
    unsigned int unk20, unk24, unk28, unk2C, unk30, unk34, unk38, unk3C;
    unsigned int unk40, unk44, unk48, unk4C, unk50, unk54, unk58, unk5C;
    unsigned int unk60, unk64, unk68, unk6C, unk70, unk74, unk78, unk7C;
    unsigned int unk80, unk84;
};
struct SearchOwner : MobileObjectBase {
    unsigned int unk88, unk8C, unk90, unk94, unk98, unk9C, unkA0;
    SearchNode entries;
    int* FUN_009b1720(int category);
};
int* SearchOwner::FUN_009b1720(int category) {
    int* found = 0;
    SearchNode* node = &entries;
    while (found == 0 && node != 0 && !node->FUN_008256d0()) {
        EntryRecord* entry = *node->FUN_006815c0();
        if (entry != 0 && entry->category == category)
            found = &entry->result;
        node = node->FUN_00726070();
    }
    return found;
}