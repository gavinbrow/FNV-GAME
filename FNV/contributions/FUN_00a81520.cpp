extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);
void* __cdecl FUN_00aa13e0(unsigned int);

struct RefCountedProperty {
    struct VTable {
        void (__thiscall *unknown)(RefCountedProperty*);
        void (__thiscall *release)(RefCountedProperty*);
    };
    VTable* vtable;
    volatile long referenceCount;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    unsigned short mode;
    unsigned short unk1a;
    int defaultIndex;
    void FUN_00a5c200();
    void releaseReference() {
        if (InterlockedDecrement(&referenceCount) == 0)
            vtable->release(this);
    }
    void addReference() { InterlockedIncrement(&referenceCount); }
};
struct PropertyHolder {
    RefCountedProperty* property;
    void set(RefCountedProperty* value) {
        if (property != value) {
            if (property != 0)
                property->releaseReference();
            property = value;
            if (value != 0)
                value->addReference();
        }
    }
};
extern PropertyHolder DAT_011f5ae8;

void __cdecl FUN_00a81520() {
    void* allocation = FUN_00aa13e0(32);
    RefCountedProperty* replacement;
    if (allocation != 0) {
        replacement = static_cast<RefCountedProperty*>(allocation);
        replacement->FUN_00a5c200();
        replacement->vtable = reinterpret_cast<RefCountedProperty::VTable*>(&DAT_0109e274);
        replacement->defaultIndex = -1;
        replacement->mode = 1;
    } else {
        replacement = 0;
    }
    DAT_011f5ae8.set(replacement);
}