struct FnvCpu_FUN_00c91090_CpuInterface {
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
    virtual void slot30();
    virtual void slot34();
    virtual void slot38();
    virtual void slot3c();
    virtual void slot40();
    virtual void slot44();
    virtual void slot48();
    virtual void slot4c();
    virtual void Invoke(int arg0);
};
struct FnvCpu_FUN_00c91090_CpuOwner {
    unsigned int unk00;
    unsigned int unk04;
    FnvCpu_FUN_00c91090_CpuInterface* target;
    void FUN_00c91090(int arg0);
};
void FnvCpu_FUN_00c91090_CpuOwner::FUN_00c91090(int arg0)
{
    target->Invoke(arg0);
}
