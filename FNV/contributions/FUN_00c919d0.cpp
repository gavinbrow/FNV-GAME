
struct EntryList {
    int* volatile entries;
    int count;
    int findIndex(int value) const {
        int total = count;
        int index = 0;
        if (total > 0) {
            int* cursor = entries;
            do {
                if (*cursor == value)
                    return index;
                ++index;
                ++cursor;
            } while (index < total);
        }
        return -1;
    }
};
struct FUN_00c919d0_Class {
    void FUN_00c919d0(int value);
};
void FUN_00c919d0_Class::FUN_00c919d0(int value) {
    EntryList& list=*(EntryList*)((char*)this+0x188);
    list.entries[list.findIndex(value)]=0;
}
