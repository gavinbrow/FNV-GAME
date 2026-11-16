struct StrArr {
    unsigned int unk00;
    unsigned int unk04;
    unsigned short unk08;
    unsigned short unk0a;
    unsigned short unk0c;
    unsigned short unk0e;
    void SetSize(unsigned int);
    void SetAt(unsigned int, char**);
};
struct BaseCall {
    unsigned int unk00;
    unsigned int unk04;
    void FUN_00a6d830(StrArr*);
};
extern const char* g_011f36bc_arg1;
extern char* __cdecl FUN_00a7d330(const char*);
extern "C" char* __cdecl FUN_00a7d370(const char*, int);
struct BaseWrap : BaseCall {
    unsigned char flags;
    void FUN_00a2f980(StrArr*);
};
void BaseWrap::FUN_00a2f980(StrArr* stream)
{
    FUN_00a6d830(stream);
    char* value = FUN_00a7d330(g_011f36bc_arg1);
    unsigned int index = stream->unk0a;
    if (index >= stream->unk08) {
        stream->SetSize(stream->unk0e + index);
    }
    stream->SetAt(index, &value);
    *(unsigned char*)&value = (flags >> 5) & 1;
    value = FUN_00a7d370("IsManagerControlled", *(int*)&value);
    index = stream->unk0a;
    if (index >= stream->unk08) {
        stream->SetSize(stream->unk0e + index);
    }
    stream->SetAt(index, &value);
}