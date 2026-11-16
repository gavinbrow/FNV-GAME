struct CpuInterface {
    virtual void slot00();
    virtual void slot04();
    virtual void Invoke();
};
struct CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    CpuInterface* target;
    void FUN_00dc89f0();
};
void CpuObject::FUN_00dc89f0()
{
    target->Invoke();
}
