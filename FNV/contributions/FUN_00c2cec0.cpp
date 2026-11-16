struct FNVArray195 {
    void* vtable;
    void* elements;
    unsigned short capacity;
    unsigned short count;
    unsigned short elementSize;
    unsigned short growBy;
    void __thiscall FUN_0096ad30(unsigned int requiredSize);
    void __thiscall FUN_0096ae90(unsigned int index, void** value);
};
struct FNVSubObject195 {
    int unk00;
    void* __thiscall FUN_00a59af0(const void* key);
};
struct GlobalObjectO2_00a7b610 { void* object; };
extern GlobalObjectO2_00a7b610 g_01202770;
extern char UNK_010bffd0;
extern char UNK_01044b44;
void* __cdecl FUN_00a7d330(void* object);
void* __cdecl FUN_00a7d370(const void* key, unsigned int attribute);
struct FNVObject195 {
    int unk00, unk04, unk08, unk0c;
    int unk10, unk14, unk18, unk1c;
    int unk20, unk24, unk28, unk2c;
    unsigned char attribute30;
    FNVSubObject195 subobject34;
    void __thiscall FUN_00c322b0(FNVArray195* storage);
    void __thiscall FUN_00c2cec0(FNVArray195* storage);
};
void __thiscall FNVObject195::FUN_00c2cec0(FNVArray195* storage) {
    FNVArray195* const array = storage;
    FUN_00c322b0(array);
    void* value = FUN_00a7d330(g_01202770.object);
    unsigned int position = array->count;
    if (position >= array->capacity) {
        array->FUN_0096ad30(position + array->growBy);
    }
    array->FUN_0096ae90(position, &value);
    value = FUN_00a7d370(&UNK_010bffd0, attribute30);
    position = array->count;
    if (position >= array->capacity) {
        array->FUN_0096ad30(position + array->growBy);
    }
    array->FUN_0096ae90(position, &value);
    value = subobject34.FUN_00a59af0(&UNK_01044b44);
    position = array->count;
    if (position >= array->capacity) {
        array->FUN_0096ad30(position + array->growBy);
    }
    array->FUN_0096ae90(position, &value);
}