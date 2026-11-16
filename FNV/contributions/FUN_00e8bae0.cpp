extern int DAT_010efdd8;
extern int DAT_010efdf8;
extern "C" void* __cdecl FUN_00aa1070(unsigned int);
extern "C" void* __cdecl FUN_00ec61c0(void*, int, unsigned int);
struct Observer {
    virtual void __stdcall Slot0();
    virtual void __stdcall Slot1();
};
struct MapProcessor {
    int* vtable;
    unsigned int bucketCount;
    void* buckets;
    unsigned int itemCount;
    int field10;
    int field14;
    int field18;
    Observer* observer1c;
    void* volatile context20;
    int index24;
    int field28;
    int field2c;
    int field30;
    int field34;
    int field38;
    unsigned char data3c[512];
    void FUN_00e8b170();
    MapProcessor* FUN_00e8bae0(void* context, Observer* observer);
};
MapProcessor* MapProcessor::FUN_00e8bae0(void* context, Observer* observer) {
    vtable = &DAT_010efdd8;
    bucketCount = 37;
    itemCount = 0;
    buckets = FUN_00aa1070(148);
    FUN_00ec61c0(buckets, 0, bucketCount * sizeof(void*));
    vtable = &DAT_010efdf8;
    field18 = 0;
    field10 = 0;
    field14 = 0;
    context20 = context;
    index24 = -1;
    observer1c = observer;
    observer->Slot1();
    field38 = 0;
    FUN_00ec61c0(data3c, 0, sizeof(data3c));
    FUN_00e8b170();
    return this;
}
