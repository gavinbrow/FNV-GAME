
struct FNVEntry {
    int unk00;
    int unk04;
    unsigned int taggedType;
};
int __cdecl FUN_00cb0fa0(const void* filter, const void* tagged);
struct FNVEntryCollection {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    FNVEntry** items;
    int count;

    FNVEntry* __thiscall FUN_00e2dfd0(const void* filter, FNVEntry* previous);
};
FNVEntry* __thiscall FNVEntryCollection::FUN_00e2dfd0(const void* filter, FNVEntry* previous)
{
    int index = 0;
    FNVEntry** slot = 0;
    while (previous && index < count && (slot = &items[index++], *slot != previous)) {
    }

    for (int next = index; next < count; ++next) {
        FNVEntry* item = items[next];
        if (!filter || !FUN_00cb0fa0(filter, reinterpret_cast<const void*>(item->taggedType & ~1u))) {
            return item;
        }
    }
    return 0;
}
