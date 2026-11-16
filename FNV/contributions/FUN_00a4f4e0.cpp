
struct FNVStream {
    virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03();
    virtual void v04(); virtual void v05(); virtual void v06(); virtual void v07();
    virtual void v08(); virtual void v09(); virtual void v10(); virtual void v11();
    virtual void SaveLink(void*);
};
struct FNVWriter {
    void* unk00;
    unsigned int written;
    void* unk08;
    unsigned int (__cdecl* Write)(FNVWriter*, const void*, unsigned int, unsigned int*, unsigned int);
    void SaveResult(const void* data) {
        unsigned int bytes = 4;
        unsigned int result = Write(this, data, 4, &bytes, 1);
        written += result;
    }
};
struct FNVBaseController {
    void __thiscall FUN_00a57c00(FNVStream*);
};
struct FNVFlipController : FNVBaseController {
    void __thiscall FUN_00a4f4e0(FNVStream*);
};
void __thiscall FNVFlipController::FUN_00a4f4e0(FNVStream* stream)
{
    FUN_00a57c00(stream);
    FNVWriter* writer = *(FNVWriter**)((char*)stream + 0x250);
    writer->SaveResult((char*)this + 0x4c);

    unsigned int count = *(unsigned short*)((char*)this + 0x42);
    writer = *(FNVWriter**)((char*)stream + 0x250);
    {
        unsigned int bytes = 4;
        writer->written += writer->Write(writer, &count, 4, &bytes, 1);
    }
    for (unsigned int i = 0; i < count; ++i) {
        void* object = (*(void***)((char*)this + 0x3c))[i];
        stream->SaveLink(object);
    }
}
