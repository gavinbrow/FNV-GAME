struct ArrayRecord { void* data; int size; int capacity; };
struct ArrayPair { ArrayRecord first; ArrayRecord second; };
struct BSAudio {};
BSAudio* __cdecl FUN_00c85750();
extern "C" void __cdecl FUN_00c908c0(void*, void*, int, int);
struct FUN_00ddacd0_shell {
    void __thiscall FUN_00dd8fe0(void* output, int elementSize, int count);
    void __thiscall FUN_00ddac60(void* output);
    void __thiscall FUN_00ddac00(void* output);
    void __thiscall FUN_00ddacd0(ArrayPair* arrays);
};
void __thiscall FUN_00ddacd0_shell::FUN_00ddacd0(ArrayPair* arrays) {
    {
        int firstCount;
        FUN_00dd8fe0(&firstCount, 4, 1);
        if (firstCount > 0) {
            for (int remaining = firstCount; remaining != 0; --remaining) {
                BSAudio* allocator = FUN_00c85750();
                void* growFunction = *(void**)((char*)allocator + 0x10);
                ArrayRecord* array = &arrays->first;
                int size = array->size;
                int needed = size + 1;
                int capacity = array->capacity & 0x3fffffff;
                if (capacity < needed) {
                    int grown = capacity * 2;
                    if (needed < grown)
                        needed = grown;
                    FUN_00c908c0(growFunction, array, needed, 16);
                }
                ++array->size;
                void* output = (char*)array->data + size * 16;
                FUN_00ddac60(output);
            }
        }
    }
    {
        int secondCount;
        FUN_00dd8fe0(&secondCount, 4, 1);
        if (secondCount > 0) {
            ArrayRecord* array = &arrays->second;
            for (int remaining = secondCount; remaining != 0; --remaining) {
                BSAudio* allocator = FUN_00c85750();
                void* growFunction = *(void**)((char*)allocator + 0x10);
                int size = array->size;
                int needed = size + 1;
                int capacity = array->capacity & 0x3fffffff;
                if (capacity < needed) {
                    int grown = capacity * 2;
                    if (needed < grown)
                        needed = grown;
                    FUN_00c908c0(growFunction, array, needed, 16);
                }
                ++array->size;
                void* output = (char*)array->data + size * 16;
                FUN_00ddac00(output);
            }
        }
    }
}
