// Reconstructed NiPSysDragModifier binary-loading routine.
struct DragObject {
    void* unk00;
    void* unk04;
    const char* objectName;
};
struct Point3Serializer {
    float x, y, z;
    void* FUN_00a59af0(const void* typeName);
};
struct StreamArray {
    void** vtable;
    void* elements;
    unsigned short capacity;
    unsigned short size;
    unsigned short activeSize;
    unsigned short growBy;
    void FUN_0096ad30(unsigned int newCapacity);
    void FUN_0096ae90(unsigned int index, void* const* value);
    __forceinline void Append(void* value) {
        unsigned int index = size;
        if (index >= capacity)
            FUN_0096ad30(index + growBy);
        FUN_0096ae90(index, &value);
    }
};
struct NiPSysDragShell : NiPSysModifier {
    DragObject* dragObject;
    Point3Serializer dragAxis;
    float percentage;
    float range;
    float falloff;
    void FUN_00c2c620(NiStream& stream);
};
extern char DAT_0102909c;
extern char DAT_010bff18;
extern char DAT_010bff0c;
extern char DAT_010bff00;
extern char DAT_01062600;
extern char DAT_010bfef0;
void* __cdecl FUN_00a7d330(void* object);
void* __cdecl FUN_00a7d5e0(const void* typeName, const void* value);
void* __cdecl FUN_00a7d550(const void* typeName, float value);
void NiPSysDragShell::FUN_00c2c620(NiStream& stream) {
    NiPSysModifier::SaveBinary(stream);
    StreamArray& array = *reinterpret_cast<StreamArray*>(&stream);
    array.Append(FUN_00a7d330(*reinterpret_cast<void**>(&g_01202768)));
    const char* name = dragObject ? dragObject->objectName : &DAT_0102909c;
    array.Append(FUN_00a7d5e0(&DAT_010bff18, name));
    array.Append(dragAxis.FUN_00a59af0(&DAT_010bff0c));
    array.Append(FUN_00a7d550(&DAT_010bff00, percentage));
    array.Append(FUN_00a7d550(&DAT_01062600, range));
    array.Append(FUN_00a7d550(&DAT_010bfef0, falloff));
}