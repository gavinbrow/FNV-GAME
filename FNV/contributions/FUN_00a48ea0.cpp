extern "C" const void* g_011f3f60;
extern "C" char DAT_01098800;
extern "C" char DAT_010987ec;

struct Stream {
    unsigned int unk00;
    unsigned int unk04;
    unsigned short unk08;
    unsigned short unk0a;
    unsigned short unk0c;
    unsigned short unk0e;

    void __thiscall FUN_0096ad30(unsigned int index);
    void __thiscall FUN_0096ae90(unsigned int index, void** value);
};
struct Storage {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    void* __thiscall FUN_00a6e190(void* value);
};
void* __cdecl FUN_00a7d330(const void* value);
void* __cdecl FUN_00a7d5a0(const void* key, void* value);

struct QuaternionInterpolator {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    Storage unk0c;
    void* unk1c;

    void __thiscall FUN_00a3cbf0(Stream* stream);
    void __thiscall FUN_00a48ea0(Stream* stream);
};

void QuaternionInterpolator::FUN_00a48ea0(Stream* stream)
{
    FUN_00a3cbf0(stream);
    void* value = FUN_00a7d330(g_011f3f60);
    unsigned int index = stream->unk0a;
    if (index >= stream->unk08)
        stream->FUN_0096ad30(index + stream->unk0e);
    stream->FUN_0096ae90(index, &value);

    value = unk0c.FUN_00a6e190(&DAT_01098800);
    index = stream->unk0a;
    if (index >= stream->unk08)
        stream->FUN_0096ad30(index + stream->unk0e);
    stream->FUN_0096ae90(index, &value);

    void* payload = unk1c;
    value = FUN_00a7d5a0(&DAT_010987ec, payload);
    index = stream->unk0a;
    if (index >= stream->unk08)
        stream->FUN_0096ad30(index + stream->unk0e);
    stream->FUN_0096ae90(index, &value);
}