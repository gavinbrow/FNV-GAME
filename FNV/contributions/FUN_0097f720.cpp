struct FUN_00999a5e0_shell
{
    void FUN_00999a5e0(int);
};

struct FUN_0097f720_target
{
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual void v4();
    virtual void v5();
    virtual void v6();
    virtual void v7();
    virtual void v8(int);
};

struct FUN_0097f720_shell
{
    int field_00;
    int field_04;
    int field_08;
    int field_0c;
    int field_10;
    int field_14;
    int field_18;
    int field_1c;
    int field_20;
    int field_24;
    int field_28;
    int field_2c;
    int field_30;
    int field_34;
    int field_38;
    int field_3c;
    int field_40;
    int field_44;
    int field_48;
    int field_4c;
    int field_50;
    int field_54;
    int field_58;
    int field_5c;
    int field_60;
    int field_64;
    int field_68;
    int field_6c;
    int field_70;
    int field_74;
    int field_78;
    int field_7c;
    int field_80;
    FUN_0097f720_target* field_84;
    FUN_0097f720_target* field_88;
    int field_8c;
    int field_90;
    int field_94;
    int field_98;
    FUN_00999a5e0_shell* field_9c;

    void FUN_0097f720(int);
};

void FUN_0097f720_shell::FUN_0097f720(int pParam)
{
    field_9c->FUN_00999a5e0(pParam);

    if (field_84 != 0)
        field_84->v8(pParam);

    if (field_88 != 0)
        field_88->v8(pParam);
}