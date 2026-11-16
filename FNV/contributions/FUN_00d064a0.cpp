typedef unsigned int Size64;
inline void* __cdecl operator new(Size64, void* p) { return p; }
struct Shape64 { void __thiscall FUN_00c90510(); };
typedef Shape64* ShapePtr64;
struct Array64 { ShapePtr64* items; int size; unsigned int capacityAndFlags; };
struct Router64 { void* unk00; void* unk04; void* unk08; void* unk0c; void* allocator; };
Router64* __cdecl FUN_00c85750();
void __cdecl FUN_00c90940(void* allocator, Array64* array, int elementSize);
struct Container64 {
    void* vtable;
    void* pad04;
    Array64 array;
    void __thiscall FUN_00d064a0(Shape64* object);
};
void Container64::FUN_00d064a0(Shape64* object) {
    if (object) {
        object->FUN_00c90510();
        Array64* collection = &array;
        Router64* router = FUN_00c85750();
        if (collection->size == (collection->capacityAndFlags & 0x3fffffff)) {
            FUN_00c90940(router->allocator, collection, 4);
        }
        ShapePtr64* location = collection->items + collection->size;
        __assume(location != 0);
        new (location) ShapePtr64(object);
        ++collection->size;
    }
}