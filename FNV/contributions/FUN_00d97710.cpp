struct Entry { unsigned short unk00; unsigned short unk02; unsigned short unk04; unsigned short unk06; unsigned short unk08; unsigned short unk0A; unsigned short unk0C; unsigned short unk0E; };
struct FUN_00d97710_class {
    int unk00; int unk04; int unk08; int unk0C; int unk10; int unk14; int unk18;
    Entry *entries;
    int count;
    void FUN_00d97710(int key);
};
void FUN_00d97710_class::FUN_00d97710(int key) {
    int i = 0;
    int n = count;
    if (n > 0) {
        Entry *entry = entries;
        do {
            union { int value; unsigned short words[2]; } identifier;
            identifier.words[0] = entry->unk06;
            identifier.words[1] = entry->unk0E;
            if (identifier.value == key) {
                entry->unk04 = 0xffff;
                entry->unk02 = 0xffff;
                entry->unk00 = 0xffff;
                entry->unk0C = 0;
                entry->unk0A = 0;
                entry->unk08 = 0;
                return;
            }
            ++i;
            entry = (Entry *)((char *)entry + 0x10);
        } while (i < n);
    }
}
