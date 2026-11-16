struct FnvCpu_FUN_00dbadf0_CpuInterface {
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
    virtual void slot50();
    virtual void slot54();
    virtual void slot58();
    virtual void slot5c();
    virtual void slot60();
    virtual void slot64();
    virtual void slot68();
    virtual void slot6c();
    virtual void slot70();
    virtual void slot74();
    virtual void slot78();
    virtual void slot7c();
    virtual void slot80();
    virtual void slot84();
    virtual void Invoke(int arg0);
};
struct FnvCpu_FUN_00dbadf0_CpuOwner {
    FnvCpu_FUN_00dbadf0_CpuInterface* target;
    void FUN_00dbadf0(int arg0);
};
void FnvCpu_FUN_00dbadf0_CpuOwner::FUN_00dbadf0(int arg0)
{
    target->Invoke(arg0);
}
