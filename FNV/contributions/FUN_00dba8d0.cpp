struct FnvCpu_FUN_00dba8d0_CpuInterface {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0c();
    virtual void slot10();
    virtual void slot14();
    virtual void slot18();
    virtual void Invoke(int arg0);
};
struct FnvCpu_FUN_00dba8d0_CpuOwner {
    FnvCpu_FUN_00dba8d0_CpuInterface* target;
    void FUN_00dba8d0(int arg0);
};
void FnvCpu_FUN_00dba8d0_CpuOwner::FUN_00dba8d0(int arg0)
{
    target->Invoke(arg0);
}
