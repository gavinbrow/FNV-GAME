struct FnvCpu_FUN_00dba910_CpuInterface {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0c();
    virtual void Invoke(int arg0);
};
struct FnvCpu_FUN_00dba910_CpuOwner {
    FnvCpu_FUN_00dba910_CpuInterface* target;
    void FUN_00dba910(int arg0);
};
void FnvCpu_FUN_00dba910_CpuOwner::FUN_00dba910(int arg0)
{
    target->Invoke(arg0);
}
