#include <xmmintrin.h>
struct __declspec(align(16)) Row { float x, y, z, w; };
struct __declspec(align(16)) Matrix44 {
    Row row0, row1, row2, row3;
};

struct __declspec(align(16)) Item {
    Matrix44 transform;
    int payload;
    void __thiscall FUN_00ddea00(const Item* source);
};

struct Allocator {
    virtual void unused0();
    virtual void unused1();
    virtual void unused2();
    virtual void unused3();
    virtual void release(void* data, unsigned int bytes);
};

struct PoolState {
    char* cursor;
    int unk04;
    int unk08;
    int unk0c;
    Allocator* allocator;
};

struct ScratchVector {
    Item* elements;
    unsigned int size;
    unsigned int encodedCapacity;
    char* originalCursor;
};

extern "C" Matrix44 DAT_01268370;
extern "C" PoolState* __cdecl FUN_00c85750();
extern "C" void __cdecl FUN_00c90940(Allocator*, const void*, unsigned int);
extern "C" void __cdecl FUN_00dddcd0(const Matrix44*, int, int, ScratchVector*, int);

void __cdecl FUN_00dde760(int a, int b, int c, int d)
{
    Item item;
    _mm_store_ps(&item.transform.row0.x, _mm_load_ps(&DAT_01268370.row0.x));
    _mm_store_ps(&item.transform.row1.x, _mm_load_ps(&DAT_01268370.row1.x));
    _mm_store_ps(&item.transform.row2.x, _mm_load_ps(&DAT_01268370.row2.x));
    _mm_store_ps(&item.transform.row3.x, _mm_load_ps(&DAT_01268370.row3.x));
    item.payload = b;
    ScratchVector vector;
    vector.elements = 0;
    vector.size = 0;
    vector.encodedCapacity = 0x80000000;
    PoolState* state = FUN_00c85750();
    char* cursor = state->cursor;
    state->cursor = cursor + 0x80;
    vector.elements = reinterpret_cast<Item*>(cursor);
    vector.encodedCapacity = 0x80000001;
    vector.originalCursor = cursor;
    state = FUN_00c85750();
    if (vector.size == (vector.encodedCapacity & 0x3fffffff)) {
        FUN_00c90940(state->allocator, &vector, 0x50);
    }
    Item* destination = vector.elements + vector.size;
    if (destination != 0)
        destination->FUN_00ddea00(&item);
    ++vector.size;
    FUN_00dddcd0(&DAT_01268370, a, c, &vector, d);
    char* finalCursor = vector.originalCursor;
    if (finalCursor == reinterpret_cast<char*>(vector.elements))
        vector.size = 0;
    FUN_00c85750()->cursor = finalCursor;
    state = FUN_00c85750();
    Allocator* currentAllocator = state->allocator;
    vector.size = 0;
    if ((vector.encodedCapacity & 0x80000000u) == 0)
        currentAllocator->release(vector.elements, (vector.encodedCapacity & 0x3fffffff) * 0x50);
}