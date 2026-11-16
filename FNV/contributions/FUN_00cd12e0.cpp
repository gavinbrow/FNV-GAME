struct FUN_00cd12e0_element {
    unsigned int value;
    void FUN_00cb0a60();
    void FUN_00cb0c10();
};
struct FUN_00cd12e0_array {
    FUN_00cd12e0_element* data;
    unsigned int size;
    unsigned int capacityFlags;
};
struct FUN_00cd12e0_router {
    unsigned int m_0;
    unsigned int m_4;
    unsigned int m_8;
    unsigned int m_c;
    void* heap;
};
FUN_00cd12e0_router* FUN_00c85750();
void __cdecl FUN_00c90940(void*, FUN_00cd12e0_array*, int);
struct FUN_00cd12e0_owner {
    void FUN_00cd12e0();
};
void FUN_00cd12e0_owner::FUN_00cd12e0() {
    FUN_00cd12e0_array* array = reinterpret_cast<FUN_00cd12e0_array*>(reinterpret_cast<char*>(this) + 0x50);
    FUN_00cd12e0_router* router = FUN_00c85750();
    if (array->size == (array->capacityFlags & 0x3fffffff)) {
        FUN_00c90940(router->heap, array, 4);
    }
    FUN_00cd12e0_element* item = array->data + array->size;
    if (item != 0) {
        item->FUN_00cb0a60();
    }
    item = array->data + array->size++;
    item->FUN_00cb0c10();
}