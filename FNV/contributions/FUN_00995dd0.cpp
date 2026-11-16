struct SearchItem { int __thiscall FUN_0044edb0(); };
struct SearchDestination { void __thiscall FUN_007cb2e0(SearchItem** item); };
struct SearchIterator {
    unsigned int __thiscall FUN_00996320();
    unsigned char __thiscall FUN_00996370(unsigned int* cursor, unsigned int* metadata, SearchItem** item);
};
struct SearchContainer { SearchIterator* __thiscall FUN_007d6bb0(); };
struct SearchOwner {
    unsigned int unk00, unk04, unk08, unk0c, unk10, unk14;
    unsigned int unk18, unk1c, unk20, unk24, unk28, unk2c;
    SearchContainer* container;
    void __thiscall FUN_00995dd0(int id, SearchDestination* destination);
};
void SearchOwner::FUN_00995dd0(int id, SearchDestination* destination)
{
    SearchIterator* cursor = container->FUN_007d6bb0();
    unsigned int currentIndex = cursor->FUN_00996320();
    unsigned int auxiliary;
    SearchItem* entry;
    while (currentIndex != 0) {
        cursor->FUN_00996370(&currentIndex, &auxiliary, &entry);
        if (entry->FUN_0044edb0() == id) {
            destination->FUN_007cb2e0(&entry);
        }
    }
}