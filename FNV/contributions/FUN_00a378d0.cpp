struct StreamWriter;
typedef unsigned int (__cdecl *WriteItemFn)(StreamWriter*, const void*, unsigned int, unsigned int*, unsigned int);
struct StreamWriter { void* interfacePtr; unsigned int totalBytes; void* auxPtr; WriteItemFn write; };
struct StreamS {
    virtual void v0(); virtual void v1(); virtual void v2(); virtual void v3(); virtual void v4(); virtual void v5();
    virtual void v6(); virtual void v7(); virtual void v8(); virtual void v9(); virtual void v10(); virtual void v11();
    virtual void WriteInterpolator(void* p);
};
struct InterpItem {
    void* interpolator; float weight; float normalizedWeight; char priority; char unk0d,unk0e,unk0f;
    float easeSpinner; float updateTime;
    void FUN_00a378d0(StreamS* stream);
};
void InterpItem::FUN_00a378d0(StreamS* stream)
{
    stream->WriteInterpolator(interpolator);
    StreamWriter* writer = *reinterpret_cast<StreamWriter**>(reinterpret_cast<char*>(stream) + 0x250);
    {
        unsigned int bytes = 4;
        writer->totalBytes += writer->write(writer, &weight, 4, &bytes, 1);
    }
    writer = *reinterpret_cast<StreamWriter**>(reinterpret_cast<char*>(stream) + 0x250);
    {
        unsigned int bytes = 4;
        writer->totalBytes += writer->write(writer, &normalizedWeight, 4, &bytes, 1);
    }
    writer = *reinterpret_cast<StreamWriter**>(reinterpret_cast<char*>(stream) + 0x250);
    {
        unsigned int bytes = 1;
        writer->totalBytes += writer->write(writer, &priority, 1, &bytes, 1);
    }
    writer = *reinterpret_cast<StreamWriter**>(reinterpret_cast<char*>(stream) + 0x250);
    {
        unsigned int bytes = 4;
        writer->totalBytes += writer->write(writer, &easeSpinner, 4, &bytes, 1);
    }
}