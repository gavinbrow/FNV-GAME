struct Entry {
    unsigned int identifier;
    unsigned int subIdentifier;
    unsigned int properties;
    unsigned int group;
    unsigned int FUN_00e7af60(unsigned int accumulated);
};
struct EntryArray {
    void* vtable;
    Entry** items;
    unsigned short capacity;
    unsigned short count;
    unsigned short elementSize;
    unsigned short growBy;
};
struct Owner {
    EntryArray& entries() {
        return *reinterpret_cast<EntryArray*>(reinterpret_cast<char*>(this) + 0x450);
    }
    Entry* FUN_00e7b190(unsigned int group, unsigned int identifier, unsigned int subIdentifier, unsigned int* accumulated);
};
Entry* Owner::FUN_00e7b190(unsigned int group, unsigned int identifier, unsigned int subIdentifier, unsigned int* accumulated)
{
    Entry* match = 0;
    for (unsigned int index = 0; index < entries().count; ++index) {
        Entry* item = entries().items[index];
        if (item && item->group == group && item->identifier == identifier && item->subIdentifier == subIdentifier) {
            match = item;
            *accumulated = item->FUN_00e7af60(*accumulated);
        }
    }
    return match;
}