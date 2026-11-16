extern "C" int DAT_01093d28;
extern "C" int DAT_01093cf8;
struct EntryObject {
    void* volatile vtable;
    int unk04;
    int unk08;
    void* volatile secondaryVtable;
    void FUN_009faf50(void* subobject);
    void FUN_009fb170();
    void FUN_009fabb0();
    void FUN_009fb1c0();
};
struct CleanupGuard {
    EntryObject* const owner;
    CleanupGuard(EntryObject* obj) : owner(obj) {
        obj->vtable = &DAT_01093d28;
        obj->secondaryVtable = &DAT_01093cf8;
    }
    ~CleanupGuard() { owner->FUN_009fabb0(); }
};
void EntryObject::FUN_009fb1c0()
{
    CleanupGuard cleanup(this);
    FUN_009faf50((void*)&secondaryVtable);
    FUN_009fb170();
}
