extern const char str_0101608c[];
struct AutoMemHelper {
    AutoMemHelper(int category, bool active, const char* file, int line);
    ~AutoMemHelper();
    void* memory;
};
struct DataListEntry {
    int* FUN_006815c0();
};
struct EntryEnumerator {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0c();
    virtual void v10();
    virtual bool v14(int data);
    bool FUN_00404d30();
    DataListEntry* FUN_0044faa0();
    DataListEntry* FUN_0044fac0(DataListEntry* current);
    bool FUN_0044f9c0();
};
bool EntryEnumerator::FUN_0044f9c0() {
    AutoMemHelper guard(9, true, str_0101608c, 0x357);
    bool succeeded = FUN_00404d30();
    if (succeeded) {
        DataListEntry* current = FUN_0044faa0();
        while (current != 0) {
            if (*current->FUN_006815c0() != 0) {
                succeeded = succeeded & v14(*current->FUN_006815c0());
            }
            current = FUN_0044fac0(current);
        }
    }
    return succeeded;
}