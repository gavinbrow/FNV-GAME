struct ChanceToHit {
    float __thiscall FUN_00a011b0();
};
struct VATSLookupList {
    bool __thiscall FUN_008256d0();
    ChanceToHit*** __thiscall FUN_006815c0(int id);
    VATSLookupList* __thiscall FUN_00726070();
};
struct VATSLookup {
    int unk00;
    VATSLookupList items;
    bool __thiscall FUN_007f7280(unsigned int index, bool byPosition);
    bool __thiscall FUN_007f7380(VATSLookupList* found, VATSLookupList* previous);
};
bool VATSLookup::FUN_007f7280(unsigned int index, bool byPosition)
{
    if (items.FUN_008256d0()) {
        return false;
    }
    VATSLookupList* previous;
    VATSLookupList* current = this ? &items : 0;
    previous = this ? &items : 0;
    if (byPosition) {
        unsigned int counter = 0;
        while (current && counter++ != index) {
            previous = current;
            current = current->FUN_00726070();
        }
    } else {
        while (current && (**current->FUN_006815c0(0xfac))->FUN_00a011b0() != index) {
            previous = current;
            current = current->FUN_00726070();
        }
    }
    return FUN_007f7380(current, previous);
}