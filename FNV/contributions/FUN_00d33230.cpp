struct FnvCpu_FUN_00d33230_CpuInterface {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0c();
    virtual void slot10();
    virtual void Invoke(int arg0);
};
struct FnvCpu_FUN_00d33230_CpuOwner {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    FnvCpu_FUN_00d33230_CpuInterface* target;
    void FUN_00d33230(int arg0);
};
void FnvCpu_FUN_00d33230_CpuOwner::FUN_00d33230(int arg0)
{
    target->Invoke(arg0);
}
