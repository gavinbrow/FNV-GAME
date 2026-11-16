extern "C" void* __cdecl FUN_00e7e880(unsigned int count);
struct Block {
    char* data;
    unsigned int count;
    Block* next;
    void Initialize(unsigned int n) {
        count = n;
        next = 0;
        if (n > 0) data = (char*)FUN_00e7e880(n);
        else data = 0;
    }
    char* At(unsigned int index) const {
        char* value;
        if (index >= count) {
            value = 0;
        } else {
            value = data + index * 104;
        }
        return value;
    }
};
struct ArrayAllocator { void* __thiscall FUN_00aa3e40(unsigned int bytes); };
extern ArrayAllocator DAT_011f6238;
struct BlockArray {
    char** data;
    unsigned int capacity;
    unsigned int size;
    Block* blocks;
    void __thiscall FUN_00a311e0(unsigned int count);
    void __thiscall FUN_00e7eb50(unsigned int count);
};
void BlockArray::FUN_00e7eb50(unsigned int count) {
    Block* memory = (Block*)DAT_011f6238.FUN_00aa3e40(sizeof(Block));
    Block* block;
    if (memory) {
        memory->Initialize(count);
        block = memory;
    } else {
        block = 0;
    }
    for (unsigned int i = 0; i < count; ++i) {
        char* value = block->At(i);
        if (size == capacity) {
            unsigned int newCapacity = capacity > 0 ? capacity * 2 : 1;
            FUN_00a311e0(newCapacity);
        }
        data[size++] = value;
    }
    block->next = blocks;
    blocks = block;
}