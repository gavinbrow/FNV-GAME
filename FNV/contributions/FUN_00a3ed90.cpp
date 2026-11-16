struct Stream {
    unsigned int flags, bytesRead;
    int (__cdecl *readProc)(Stream*, void*, unsigned int, unsigned int*, int);
    __forceinline int Read(void* dst, unsigned int count) {
        unsigned int actual = count;
        return readProc(this, dst, count, &actual, 1);
    }
};
struct Source {
    Stream* stream() { return *reinterpret_cast<Stream**>(reinterpret_cast<char*>(this) + 0x24c); }
    void __thiscall FUN_00a645b0();
};
void __stdcall FUN_00aa0ac0(Source*);
struct PathData {
    unsigned int unk00, unk04, unk08;
    unsigned short channel, unk0e;
    unsigned int unk10, unk14, unk18, unk1c, unk20, unk24;
    unsigned int value28, value2c;
    unsigned short channel30, unk32;
    unsigned int unk34, value38;
    void __thiscall FUN_00a3ed90(Source*);
};
void PathData::FUN_00a3ed90(Source* source) {
    FUN_00aa0ac0(source);
    Stream* stream = source->stream();
    stream->bytesRead += stream->Read(&channel, 2);
    unsigned int value;
    stream = source->stream();
    stream->bytesRead += stream->Read(&value, 4);
    value38 = value;
    stream = source->stream();
    stream->bytesRead += stream->Read(&value28, 4);
    stream = source->stream();
    stream->bytesRead += stream->Read(&value2c, 4);
    stream = source->stream();
    stream->bytesRead += stream->Read(&channel30, 2);
    source->FUN_00a645b0();
    source->FUN_00a645b0();
}