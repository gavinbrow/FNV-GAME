struct CpuInterface {
    virtual void slot00();
    virtual void Invoke();
};
struct CpuObject {
    CpuInterface* target;
    void FUN_00dbac10();
};
void CpuObject::FUN_00dbac10()
{
    target->Invoke();
}
