extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" const void* DAT_010a08ac;
extern "C" const void* DAT_010a080c;
void __cdecl NiFree(void*);
struct NiRefObject {
    virtual void Reserved();
    virtual void Release();
    volatile long referenceCount;
};
struct NiObjectShell {
    void* volatile vtable;
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
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    void* allocation;
    unsigned int capacity;
    unsigned int length;
    unsigned int increment;
    unsigned int unk70;
    unsigned int unk74;
    unsigned int unk78;
    unsigned int unk7c;
    unsigned int unk80;
    unsigned int unk84;
    unsigned int unk88;
    unsigned int unk8c;
    NiRefObject* volatile reference;
    void FUN_00a5d3d0();
    void FUN_00a98240();
};
void NiObjectShell::FUN_00a98240() {
    vtable = (void*)&DAT_010a08ac;
    NiRefObject* oldReference = reference;
    if (oldReference) {
        if (InterlockedDecrement(&oldReference->referenceCount) == 0)
            oldReference->Release();
        reference = 0;
    }
    if (allocation) {
        NiFree(allocation);
        increment = 0;
        length = 0;
        capacity = 0;
        allocation = 0;
    }
    NiRefObject* lastReference = reference;
    if (lastReference) {
        if (InterlockedDecrement(&lastReference->referenceCount) == 0)
            lastReference->Release();
    }
    vtable = (void*)&DAT_010a080c;
    FUN_00a5d3d0();
}