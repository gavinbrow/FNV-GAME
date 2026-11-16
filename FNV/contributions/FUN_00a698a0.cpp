struct FUN_00a698a0_stream;
typedef int (__cdecl *FUN_00a698a0_write_fn)(FUN_00a698a0_stream*, const void*, int, int*, int);
struct FUN_00a698a0_stream { int unk00; int bytesWritten; int unk08; FUN_00a698a0_write_fn write; };
struct FUN_00a698a0_class
{
    int unk00; int unk04; int unk08; int unk0c;
    void __thiscall FUN_00a698a0(void* context);
};
void FUN_00a698a0_class::FUN_00a698a0(void* context)
{
    FUN_00a698a0_stream* stream = *(FUN_00a698a0_stream**)((char*)context + 0x250);
    int size = 4;
    { int written = 4; stream->bytesWritten += stream->write(stream, this, size, &written, 1); }
    stream = *(FUN_00a698a0_stream**)((char*)context + 0x250);
    { int written = 4; stream->bytesWritten += stream->write(stream, (char*)this + 4, size, &written, 1); }
    stream = *(FUN_00a698a0_stream**)((char*)context + 0x250);
    { int written = 4; stream->bytesWritten += stream->write(stream, (char*)this + 8, size, &written, 1); }
    stream = *(FUN_00a698a0_stream**)((char*)context + 0x250);
    { int written = 4; stream->bytesWritten += stream->write(stream, (char*)this + 12, size, &written, 1); }
}
