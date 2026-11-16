struct FUN_00854c80_shell {
    virtual ~FUN_00854c80_shell();
    int m_04;
    int m_08;
    int m_0C;
    FUN_00854c80_shell(int formType);
};

struct FUN_0096a2d0_shell {
    int m_10;
    int m_14;
    FUN_0096a2d0_shell();
};

struct FUN_00853810 : FUN_00854c80_shell {
    FUN_0096a2d0_shell m_data;
    int m_18;
    FUN_00853810();
    virtual ~FUN_00853810();
};

FUN_00853810::FUN_00853810() : FUN_00854c80_shell(0x25) {
    m_18 = 0;
}
