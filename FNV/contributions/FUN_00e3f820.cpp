struct HavokString { char* text; };
struct EnvironmentVariable { HavokString name; HavokString value; };
struct HavokAllocator {
    virtual ~HavokAllocator();
    virtual void* blockAlloc(int);
    virtual void blockFree(void*, int);
    virtual void* bufAlloc(int&);
    virtual void bufFree(void*, int);
};
HKXMemoryRouter* __cdecl FUN_00c85750();
void __fastcall FUN_00cb0c00(HavokString* string);
struct EnvironmentArray {
    EnvironmentVariable* data;
    int size;
    int capacityAndFlags;

    __forceinline void release() {
        HavokAllocator* allocator = reinterpret_cast<HavokAllocator*>(FUN_00c85750()->manager);
        EnvironmentVariable* entry = data;
        if (size > 0) {
            int remaining = size;
            do {
                FUN_00cb0c00(&entry->value);
                FUN_00cb0c00(&entry->name);
                ++entry;
            } while (--remaining != 0);
        }
        size = 0;
        if ((static_cast<unsigned int>(capacityAndFlags) & 0x80000000u) == 0)
            allocator->bufFree(data, (capacityAndFlags & 0x3fffffff) * sizeof(EnvironmentVariable));
        data = 0;
        capacityAndFlags = 0x80000000;
    }
};
struct EnvironmentLayout {
    void** vtable;
    unsigned short memoryFlags;
    short referenceCount;
    EnvironmentArray variables;
};
hkBaseObject::~hkBaseObject() {}
void HKXEnvironmentStandIn::FUN_00e3f820() {
    EnvironmentLayout* environment = reinterpret_cast<EnvironmentLayout*>(this);
    environment->variables.release();
    reinterpret_cast<hkBaseObject*>(environment)->hkBaseObject::~hkBaseObject();
}