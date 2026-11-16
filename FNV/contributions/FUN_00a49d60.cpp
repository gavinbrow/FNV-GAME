
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern int DAT_0109893c;
struct RefObject {
    virtual void GetRTTI();
    virtual void DeleteThis();
    volatile long referenceCount;
    void DecRefCount() { if (InterlockedDecrement(&referenceCount) == 0) DeleteThis(); }
};
struct RefPointer {
    RefObject* object;
    void Clear() {
        if (object) {
            object->DecRefCount();
            object = 0;
        }
    }
    void Release() { if (object) object->DecRefCount(); }
};
struct ParentData {
    void* vtable;
unsigned int unk04;
unsigned int unk08;
unsigned int unk0c;
unsigned int unk10;
unsigned int unk14;
unsigned int unk18;
unsigned int unk1c;
unsigned int unk20;
unsigned int unk24;
unsigned int unk28;
unsigned int unk2c;
unsigned int unk30;
unsigned int unk34;
unsigned int unk38;
unsigned int unk3c;
    void FUN_00a6d290();
};
void __cdecl FUN_00aa10f0(void*);
struct FUN_00a49d60 : public ParentData {
    RefPointer first;
    RefPointer second;
    void* resource;
    ~FUN_00a49d60();
};
FUN_00a49d60::~FUN_00a49d60() {
    vtable = &DAT_0109893c;
    first.Clear();
    second.Clear();
    FUN_00aa10f0(resource);
    second.Release();
    first.Release();
    ParentData::FUN_00a6d290();
}
