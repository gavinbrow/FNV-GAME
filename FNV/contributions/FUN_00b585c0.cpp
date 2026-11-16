extern void* __cdecl FUN_00ec61c0(void* dest, int value, unsigned int count);
extern void* __cdecl FUN_00aa1070(unsigned int size);

struct MapBase_00b585c0 {
    unsigned int hashSize;
    void** hashTable;
    unsigned int allocatorCount;

    MapBase_00b585c0(unsigned int size) : hashSize(size), allocatorCount(0) {
        hashTable = static_cast<void**>(FUN_00aa1070(hashSize * sizeof(void*)));
        FUN_00ec61c0(hashTable, 0, hashSize * sizeof(void*));
    }
    virtual ~MapBase_00b585c0() {}
};
struct Map_00b585c0 : MapBase_00b585c0 {
    explicit Map_00b585c0(unsigned int size) : MapBase_00b585c0(size) {}
    virtual ~Map_00b585c0() {}
};
Map_00b585c0* __cdecl FUN_00b585c0() {
    static Map_00b585c0 map(37);
    return &map;
}