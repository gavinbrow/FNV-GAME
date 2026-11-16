struct FnvCpu_FUN_00e36f50_CpuInterface {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0c();
    virtual void slot10();
    virtual void Invoke(int arg0);
};
struct FnvCpu_FUN_00e36f50_CpuOwner {
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
    FnvCpu_FUN_00e36f50_CpuInterface* target;
    void FUN_00e36f50(int arg0);
};
void FnvCpu_FUN_00e36f50_CpuOwner::FUN_00e36f50(int arg0)
{
    target->Invoke(arg0);
}
