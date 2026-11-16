struct Device {
    virtual void slot00() = 0;
    virtual void slot04() = 0;
    virtual void slot08() = 0;
    virtual void slot0c() = 0;
    virtual void Release(void* handle, unsigned int bytes) = 0;
};
struct Holder { int unk00; int unk04; int unk08; int unk0c; Device* device; };
extern void* __cdecl FUN_00c85750();
struct FUN_00cd27f0 {
    virtual void v0() = 0;
    int unk04;
    int buffer2;
    int unk0c;
    int count2;
    int unk14; int unk18; int unk1c; int unk20; int unk24; int unk28;
    int buffer1;
    volatile int unk30;
    int count1;
    virtual ~FUN_00cd27f0();
};
FUN_00cd27f0::~FUN_00cd27f0() {
    Holder* holder = (Holder*)FUN_00c85750();
    Device* device = holder->device;
    int count = count1;
    unk30 = 0;
    if ((unsigned int)count & 0x80000000) goto skipFirstRelease;
    {
        unsigned int bytes = (count & 0x3fffffff) * 4;
        device->Release((void*)buffer1, bytes);
    }
skipFirstRelease:
    buffer1 = 0;
    count1 = 0x80000000;
    holder = (Holder*)FUN_00c85750();
    device = holder->device;
    int secondCount = count2;
    unk0c = 0;
    if ((unsigned int)secondCount & 0x80000000) goto skipSecondRelease;
    {
        unsigned int bytes = (secondCount & 0x3fffffff) * 4;
        device->Release((void*)buffer2, bytes);
    }
skipSecondRelease:
    buffer2 = 0;
    count2 = 0x80000000;
}

