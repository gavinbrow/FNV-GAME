char* __cdecl FUN_00a7d330(char const*);
char* __cdecl FUN_00a7d370(char const*, bool);
template<class T> struct NiTMallocInterface {};
template<class T, class I> struct NiTPrimitiveArray { void* unk00; int unk04; unsigned short capacity; unsigned short size; unsigned short unk0c; unsigned short growth; void SetSize(unsigned int); void SetAt(unsigned int, T&); };
struct StrArr : NiTPrimitiveArray<char*, NiTMallocInterface<char*> > {};
struct FUN_00a62a40_this { void FUN_00a5d850(StrArr*); };
struct Owner : FUN_00a62a40_this { unsigned int unk00; unsigned int unk04; unsigned int unk08; unsigned int unk0c; unsigned int unk10; unsigned int unk14; unsigned char m_bDither; void FUN_00a9a670(StrArr*); };
union Temporary { char* text; bool flag; };
void Owner::FUN_00a9a670(StrArr* array) {
    FUN_00a5d850(array);
    Temporary value;
    value.text = FUN_00a7d330((char const*)g_011f5f48);
    unsigned int index = array->size;
    if (index >= array->capacity) array->SetSize(index + array->growth);
    array->SetAt(index, value.text);
    value.flag = (m_bDither & 1) != 0;
    value.text = FUN_00a7d370("m_bDither", value.flag);
    index = array->size;
    if (index >= array->capacity) array->SetSize(index + array->growth);
    array->SetAt(index, value.text);
}
