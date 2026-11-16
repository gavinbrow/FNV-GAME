struct FUN_009fd270_class {
    int __thiscall FUN_009fd270(int);
};

struct FUN_009fe3f0_class {
    int m_00;
    int m_04;
    int m_08;
    int m_0c;
    int m_10;
    int m_14;
    int m_18;
    int m_1c;
    int m_20;
    int m_24;
    int m_28;
    int m_2c;
    int m_30;
    int m_34;
    int m_38;
    int m_3c;
    int m_40;
    int m_44;
    int m_48;
    int m_4c;
    FUN_009fd270_class m_50;
    int m_54;
    int m_58;
    int m_5c;
    int m_60;
    int m_64;
    int m_68;
    int m_6c;

    int __thiscall FUN_009fe3f0(int);
};

extern void (__stdcall *DAT_00fdf0d0)(void*);

int __thiscall FUN_009fe3f0_class::FUN_009fe3f0(int value)
{
    if (m_50.FUN_009fd270(value)) {
        DAT_00fdf0d0(reinterpret_cast<void*>(m_6c));
        return 0;
    }

    return static_cast<int>(0x8007000e);
}