struct ActionDescriptor
{
    bool _Call_439090();
};

struct SaveFormHeader;
struct TESSaveLoadGame
{
    SaveFormHeader* GetCurrentFormHeader();
};

struct InterfaceManager_helper
{
    Tile* FUN_00586150();
};

int __fastcall FUN_00778970(char*);
int __fastcall FUN_009e32d0(char*);
unsigned int __fastcall FUN_0044edb0(void*);

struct FUN_009cde10_shell
{
    virtual void vfn_00();
    virtual void vfn_04();
    virtual void vfn_08();
    virtual void vfn_0c();
    virtual void vfn_10();
    virtual void vfn_14();
    virtual void vfn_18();
    virtual void vfn_1c();
    virtual void vfn_20();
    virtual void vfn_24();
    virtual void vfn_28();
    virtual void vfn_2c();
    virtual void vfn_30();
    virtual int GetActionType();
    int GetSection();
    bool FUN_0097be60(int);
    ActionDescriptor* FUN_0097be80(char*);
    ActionDescriptor* FUN_0097b940(ActionDescriptor*);
};

struct Twin_00639b40
{
    const char* GetEntryPoint();
};

struct CombatController;

bool __cdecl FUN_0097bd20(CombatController* controller, int value)
{
    FUN_009cde10_shell* piStack_c2;
    FUN_009cde10_shell* iStack_c;
    int iStack_8;
    FUN_009cde10_shell* piStack4;
    FUN_009cde10_shell* piStack_18;
    struct TargetTemp
    {
        int a;
        int b;
        int c;
    } auStack2;

    piStack_c2 = (FUN_009cde10_shell*)((TESSaveLoadGame*)controller)->GetCurrentFormHeader();
    if (piStack_c2 == 0)
        return false;

    iStack_c = (FUN_009cde10_shell*)FUN_00778970(
        (char*)((InterfaceManager_helper*)controller)->FUN_00586150());
    if (iStack_c == 0 || iStack_c->GetSection() != value)
        return false;

    iStack_8 = piStack_c2->GetActionType();
    if (iStack_8 == 6)
    {
        piStack4 = piStack_c2;
        if (iStack_c->GetSection() != (int)((Twin_00639b40*)piStack4)->GetEntryPoint())
            return false;

        if (FUN_0044edb0(iStack_c) != 0)
        {
            if (FUN_0044edb0(iStack_c) != FUN_009e32d0((char*)piStack4))
                return false;
        }
        else
        {
            if (iStack_c->FUN_0097b940(
                    piStack4->FUN_0097be80((char*)&auStack2))->_Call_439090())
                return false;
        }

        if (iStack_c->FUN_0097be60(1))
            return false;
    }
    else
    {
        if (iStack_8 == 4)
        {
            piStack_18 = piStack_c2;
            if (!iStack_c->FUN_0097be60(1))
                return false;

            if (iStack_c->GetSection() != piStack_18->GetSection())
                return false;
        }
        else
        {
            return false;
        }
    }

    return true;
}

