extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);

struct ReferenceObject {
    virtual void RetainUnused();
    virtual void Destroy();
    volatile long referenceCount;
    void DecRefCount() {
        if (InterlockedDecrement(&referenceCount) == 0) {
            Destroy();
        }
    }
    void IncRefCount() { InterlockedIncrement(&referenceCount); }
};

struct FUN_00b58140_Class {
    unsigned int unk00;
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
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6c;
    unsigned int unk70;
    unsigned int unk74;
    unsigned int unk78;
    unsigned int copiedValue7c;
    ReferenceObject* reference80;
    unsigned int copiedValue84;
    unsigned int copiedValue88;
    void __thiscall FUN_00b702b0(FUN_00b58140_Class* destination, unsigned int flags);
    void __thiscall FUN_00b58140(FUN_00b58140_Class* destination, unsigned int flags);
};

void FUN_00b58140_Class::FUN_00b58140(FUN_00b58140_Class* destination, unsigned int flags) {
    FUN_00b702b0(destination, flags);
    if (destination->reference80 != reference80) {
        if (destination->reference80) {
            destination->reference80->DecRefCount();
        }
        destination->reference80 = reference80;
        if (destination->reference80) {
            destination->reference80->IncRefCount();
        }
    }
    destination->copiedValue84 = copiedValue84;
    destination->copiedValue88 = copiedValue88;
    destination->copiedValue7c = copiedValue7c;
}