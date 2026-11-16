struct FnvCpu_FUN_00e063e0_CpuInterface {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0c();
    virtual void Invoke(int arg0);
};
struct FnvCpu_FUN_00e063e0_CpuOwner {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    FnvCpu_FUN_00e063e0_CpuInterface* target;
    void FUN_00e063e0(int arg0);
};
void FnvCpu_FUN_00e063e0_CpuOwner::FUN_00e063e0(int arg0)
{
    target->Invoke(arg0);
}
