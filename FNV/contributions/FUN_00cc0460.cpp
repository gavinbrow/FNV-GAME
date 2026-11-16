struct CpuInterface {
    virtual void slot00();
    virtual void slot04();
    virtual void slot08();
    virtual void slot0c();
    virtual void slot10();
    virtual void Invoke();
};
struct CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    CpuInterface* target;
    void FUN_00cc0460();
};
void CpuObject::FUN_00cc0460()
{
    target->Invoke();
}
