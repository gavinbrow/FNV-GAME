extern char const* const g_011f4024_arg1;
char* __cdecl FUN_00a7d330(char const*);
char* __cdecl FUN_00a7d510(char const*, unsigned int);
template<class T> struct NiTMallocInterface {};
template<class T, class I> struct NiTPrimitiveArray {
    void* unk00; int unk04;
    unsigned short capacity; unsigned short size; unsigned short unk0c; unsigned short growth;
    void SetSize(unsigned int);
    void SetAt(unsigned int, T&);
};
typedef NiTPrimitiveArray<char*, NiTMallocInterface<char*> > StringArray;
struct Base { void FUN_00a58200(StringArray*); };
struct Owner : Base {
    void* unk00; int unk04; int unk08; int unk0c; int unk10; int unk14;
    int unk18; int unk1c; int unk20; int unk24; int unk28; unsigned int value2c;
    void FUN_00a51d80(StringArray*);
};
void Owner::FUN_00a51d80(StringArray* array) {
    FUN_00a58200(array);
    char* value = FUN_00a7d330(g_011f4024_arg1);
    unsigned int index = array->size;
    if (index >= array->capacity)
        array->SetSize(index + array->growth);
    array->SetAt(index, value);
    value = FUN_00a7d510("m_kColorACPHandle", value2c);
    index = array->size;
    if (index >= array->capacity)
        array->SetSize(index + array->growth);
    array->SetAt(index, value);
}



