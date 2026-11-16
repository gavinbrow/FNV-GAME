struct ValueBlock {
    void FUN_00d33330(ValueBlock* destination);
};

struct Callback {
    virtual void Reserved00();
    virtual void Reserved04();
    virtual void Reserved08();
    virtual void Reserved0c();
    virtual void Reserved10();
    virtual void Reserved14();
    virtual void Reserved18();
    virtual void Reserved1c();
    virtual void OnValueChange(unsigned int identifier, void* data);
};

void __cdecl FUN_00ec44d0(void* target, const void* input, unsigned int byteCount);

struct Container {
    unsigned int tag;
    void FUN_00d33600(void* unusedA, void* unusedB, char* source, Callback* callback);
};

void Container::FUN_00d33600(void* unusedA, void* unusedB, char* source, Callback* callback)
{
    float sourceTime = *reinterpret_cast<float*>(source + 0x3030);
    char* destination = reinterpret_cast<char*>(this);

    if (sourceTime != *reinterpret_cast<float*>(destination + 0x1030)) {
        callback->OnValueChange(*reinterpret_cast<unsigned int*>(source + 4), source + 0x3050);
        reinterpret_cast<ValueBlock*>(source + 0x3010)->FUN_00d33330(reinterpret_cast<ValueBlock*>(destination + 0x1010));
    }

    *reinterpret_cast<unsigned int*>(source) = tag;
    void* output = *reinterpret_cast<void**>(source + 0x3080);
    if (output != 0) {
        FUN_00ec44d0(output, destination + 4, 0x1008);
    }
}
