struct CpuObject;
struct AudioInterface {
    virtual void reserved00();
    virtual void reserved04();
    virtual void dispatch(CpuObject* object, unsigned short value);
};
struct AudioSystem {
    int unk00; int unk04; int unk08; int unk0c;
    AudioInterface* unk10;
};
extern void* __cdecl FUN_00c85750();
struct CpuObject {
    int unk00;
    unsigned short unk04;
    void FUN_00e01d40();
    CpuObject* FUN_00e01dd0(bool enabled);
};
CpuObject* CpuObject::FUN_00e01dd0(bool enabled) {
    FUN_00e01d40();
    if (enabled & 1) {
        AudioSystem* system = static_cast<AudioSystem*>(FUN_00c85750());
        system->unk10->dispatch(this, unk04);
    }
    return this;
}
