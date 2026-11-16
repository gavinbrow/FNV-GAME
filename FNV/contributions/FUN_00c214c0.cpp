extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
struct ReferenceSource {
    unsigned int FUN_00a63460();
    NiRefObject* FUN_00a63430();
};
struct ReferenceArray {
    void FUN_0060bef0(unsigned int count);
    void FUN_004b0310(unsigned int index, NiRefObject** pointer);
};
struct ReferenceContainer {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    ReferenceArray array;
    void FUN_00c31650(ReferenceSource* source);
    void FUN_00c214c0(ReferenceSource* source);
};
void ReferenceContainer::FUN_00c214c0(ReferenceSource* source) {
    FUN_00c31650(source);
    unsigned int count = source->FUN_00a63460();
    ReferenceArray* array = &this->array;
    array->FUN_0060bef0(count);
    for (unsigned int index = 0; index < count; ++index) {
        NiRefObject* object = source->FUN_00a63430();
        NiRefObject* handle = object;
        if (object != 0)
            InterlockedIncrement(&object->refCount);
        array->FUN_004b0310(index, &handle);
        if (object != 0 && InterlockedDecrement(&object->refCount) == 0)
            object->DeleteThis();
    }
}