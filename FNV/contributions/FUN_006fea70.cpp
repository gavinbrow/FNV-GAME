#include "h_74712c1d3c73.h"

struct FUN_00974d90_Class
{
    bool __thiscall FUN_00974d90();
    void __thiscall FUN_006faa90(float value);
};

struct FUN_006fea70_Class
{
    void* m_00;
    int m_04;
    int m_08;
    int m_0c;
    FUN_00974d90_Class* m_10;
    int m_14;
    int m_18;
    int m_1c;

    FUN_006fea70_Class* m_20[4];

    unsigned char m_30;
    unsigned char m_31;
    unsigned char m_32;
    unsigned char m_33;
    unsigned char m_34;
    unsigned char m_35;
    unsigned char m_36;
    unsigned char m_37;
    unsigned char m_38;
    unsigned char m_39;
    unsigned char m_3a;
    unsigned char m_3b;
    unsigned char m_3c;
    unsigned char m_3d;
    unsigned char m_3e;
    unsigned char m_3f;
    unsigned char m_40;
    unsigned char m_41;
    unsigned char m_42;
    unsigned char m_43;
    unsigned char m_44;
    unsigned char m_45;
    unsigned char m_46;
    unsigned char m_47;
    unsigned char m_48;
    unsigned char m_49;
    unsigned char m_4a;
    unsigned char m_4b;
    unsigned char m_4c;
    unsigned char m_4d;
    unsigned char m_4e;
    unsigned char m_4f;
    unsigned char m_50;
    unsigned char m_51;
    unsigned char m_52;
    unsigned char m_53;
    unsigned char m_54;

    unsigned char m_55;
    unsigned char m_56;
    unsigned char m_57;
    unsigned char m_58;
    unsigned char m_59;
    unsigned char m_5a;
    unsigned char m_5b;
    unsigned char m_5c;
    unsigned char m_5d;

    float __thiscall FUN_006feb20(int value);
    void __thiscall FUN_006ff3f0();
    bool __thiscall FUN_006fb150();

    void __thiscall FUN_006fea70(int value);
};

void FUN_006fea70_Class::FUN_006fea70(int value)
{
    if (m_10 != 0 && m_10->FUN_00974d90())
    {
        m_10->FUN_006faa90(FUN_006feb20(value));

        if (m_54 != 0)
        {
            FUN_006ff3f0();
        }

        if (!FUN_006fb150() && m_5d != 0)
        {
            return;
        }
    }

    if (m_20[0] != 0)
    {
        int index;

        for (index = 0; index < 4; ++index)
        {
            m_20[index]->FUN_006fea70(value);
        }
    }
}