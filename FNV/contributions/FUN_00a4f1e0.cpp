
extern "C" void* g_011f3fcc;
extern int DAT_01099270;

struct StreamStub {
    unsigned int unk00;
    unsigned int unk04;
    unsigned short unk08;
    unsigned short unk0A;
    unsigned short unk0C;
    unsigned short unk0E;
    void FUN_0096ad30(unsigned int offset);
    void FUN_0096ae90(unsigned int index, void** result);
};

void __stdcall FUN_00a57420(StreamStub* stream);
void* __cdecl FUN_00a7d330(void* source);
void* __cdecl FUN_00a7d4d0(int* name, void* object);

struct ControllerStub {
    int unk00, unk04, unk08, unk0C;
    int unk10, unk14, unk18, unk1C;
    int unk20, unk24, unk28, unk2C;
    int unk30, unk34, unk38, unk3C;
    void* unk40;
    void FUN_00a4f1e0(StreamStub* stream);
};

void ControllerStub::FUN_00a4f1e0(StreamStub* stream)
{
    FUN_00a57420(stream);
    void* value = FUN_00a7d330(g_011f3fcc);
    unsigned int index = stream->unk0A;
    if (index >= stream->unk08)
        stream->FUN_0096ad30(index + stream->unk0E);
    stream->FUN_0096ae90(index, &value);
    value = FUN_00a7d4d0(&DAT_01099270, unk40);
    index = stream->unk0A;
    if (index >= stream->unk08)
        stream->FUN_0096ad30(index + stream->unk0E);
    stream->FUN_0096ae90(index, &value);
}
