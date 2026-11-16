struct SelectedRecord { int x; int y; int z; };
extern void* selectionContext;
int __cdecl FUN_00828b20(const void*, const void*);
void __cdecl FUN_00ec6f20(int, int, int, int);
struct SelectionPredicate { bool FUN_00828f00(int, SelectedRecord*); };
struct RecordSelector { bool FUN_00828cb0(void* context, int flags, SelectedRecord* output); };
bool RecordSelector::FUN_00828cb0(void* context, int flags, SelectedRecord* output)
{
    SelectedRecord* entries = 0;
    int count = ((FUN_00828da0_shell*)this)->FUN_00828da0((int)&entries, (int)context, flags);
    if (count <= 0 || entries == 0)
        return false;
    int index = 0;
    selectionContext = context;
    FUN_00ec6f20((int)entries, count, sizeof(SelectedRecord), (int)&FUN_00828b20);
    index = 0;
    while (index < count && !((SelectionPredicate*)this)->FUN_00828f00(flags, &entries[index])) {
        ++index;
    }
    if (index < count) {
        *output = entries[index];
        SelectedRecord* selected = entries;
        _Deallocate(selected);
        return true;
    } else {
        SelectedRecord* discarded = entries;
        _Deallocate(discarded);
        return false;
    }
}
