struct FNVAllocator {
    virtual void Release();
    virtual void* Allocate(unsigned int bytes);
};
struct FNVMemoryManager {
    FNVAllocator* GetAllocator() {
        return *reinterpret_cast<FNVAllocator**>(reinterpret_cast<char*>(this) + 0x10);
    }
};
FNVMemoryManager* __cdecl FUN_00c85750();

struct FNVArray {
    int* values;
    unsigned short size;
    unsigned short flags;
    FNVArray() : values(0), size(0), flags(0x8000) {}
};
struct FNVBuffers {
    FNVArray spare;
    FNVArray elements;
    static void* operator new(unsigned int bytes) {
        return FUN_00c85750()->GetAllocator()->Allocate(bytes);
    }
};
void __cdecl FUN_00d06cb0(FNVArray*, unsigned int);
struct FNVOwner {
    FNVBuffers*& Buffers() {
        return *reinterpret_cast<FNVBuffers**>(reinterpret_cast<char*>(this) + 0x214);
    }
    void FUN_00c9c5b0(int value);
};
void FNVOwner::FUN_00c9c5b0(int value) {
    if (Buffers() == 0) {
        Buffers() = new FNVBuffers;
    }
    FNVArray& array = Buffers()->elements;
    for (int i = 0; i < array.size; ++i) {
        if (!array.values[i]) {
            if (i >= 0) {
                array.values[i] = value;
                return;
            }
            break;
        }
    }
    if (array.size == (array.flags & 0x3fff)) {
        FUN_00d06cb0(&array, sizeof(int));
    }
    array.values[array.size] = value;
    ++array.size;
}
