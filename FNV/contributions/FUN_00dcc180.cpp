struct FUN_00dcc180_Interface
{
    virtual void FUN_00dcc180_00();
    virtual void FUN_00dcc180_01();
    virtual void FUN_00dcc180_02();
    virtual void FUN_00dcc180_03(unsigned char* value);
};

struct FUN_00dcc180_Class
{
    int unk00;
    int unk04;
    FUN_00dcc180_Interface* unk08;

    unsigned char* __thiscall FUN_00dcc180(unsigned char* value);
};

unsigned char* __thiscall FUN_00dcc180_Class::FUN_00dcc180(unsigned char* value)
{
    if (unk08)
        unk08->FUN_00dcc180_03(value);
    else
        *value = 0;

    return value;
}