
struct BinaryReader {
    void* unk00;
    unsigned int bytesRead;
    unsigned int (__cdecl *read)(BinaryReader*, void*, unsigned int, unsigned int*, unsigned int);
    void readBlock(void* output, unsigned int bytes, unsigned int unitValue) {
        unsigned int unit = unitValue;
        bytesRead += read(this, output, bytes, &unit, 1);
    }
};
struct DataSource {
    BinaryReader* reader() const {
        return *reinterpret_cast<BinaryReader* const*>(reinterpret_cast<const char*>(this) + 0x24c);
    }
};
void __stdcall FUN_00a5d610(DataSource*);
struct MMExtra { void* _Allocate(unsigned int); };
struct ReadState { unsigned int elementCount; };
struct MemoryBlock {
    unsigned int value;
    MemoryBlock() { }
    static void* operator new[](unsigned int size) {
        return reinterpret_cast<MMExtra&>(g_memoryManager)._Allocate(size);
    }
};
struct Observer { void** vtable; };
extern Observer* DAT_011f4748;
struct DataArray {
    unsigned int unk00;
    unsigned int unk04;
    bool enabled;
    unsigned int count;
    unsigned int unk10;
    MemoryBlock* values;
    void FUN_00a8b2c0(DataSource* source);
};
void DataArray::FUN_00a8b2c0(DataSource* source) {
    FUN_00a5d610(source);
    ReadState currentRead;

    unsigned char enabledByte;
    BinaryReader* reader = source->reader();
    reader->readBlock(&enabledByte, 1, 1);
    enabled = enabledByte != 0;

    reader = source->reader();
    reader->readBlock(&currentRead.elementCount, 4, 4);
    if (currentRead.elementCount != count) {
        g_memoryManager._DeallocateAlias(values);
        count = currentRead.elementCount;
        values = new MemoryBlock[currentRead.elementCount];
    }

    reader = source->reader();
    reader->readBlock(values, count * sizeof(MemoryBlock), 1);
    Observer* observer = DAT_011f4748;
    if (observer) {
        typedef void (__thiscall *OnRead)(Observer*, DataArray*);
        (reinterpret_cast<OnRead>(observer->vtable[0x150 / 4]))(observer, this);
    }
}
