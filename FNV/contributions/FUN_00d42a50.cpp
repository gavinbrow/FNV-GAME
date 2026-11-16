struct FnvCpu_FUN_00d42a50_CpuInterface {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0c();
    virtual void slot10();
    virtual void slot14();
    virtual void slot18();
    virtual void slot1c();
    virtual void slot20();
    virtual void slot24();
    virtual void slot28();
    virtual void slot2c();
    virtual void Invoke(int arg0);
};
struct FnvCpu_FUN_00d42a50_CpuOwner {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    FnvCpu_FUN_00d42a50_CpuInterface* target;
    void FUN_00d42a50(int arg0);
};
void FnvCpu_FUN_00d42a50_CpuOwner::FUN_00d42a50(int arg0)
{
    target->Invoke(arg0);
}
