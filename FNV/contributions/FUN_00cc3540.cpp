extern int DAT_0102016c;
extern int DAT_0102009c;
extern int DAT_010c9634;
extern int DAT_01268154;
extern int DAT_01268118;
extern int DAT_012685b8;

struct C200125Base
{
    void FUN_00c87c30();
};

struct C200125Object : C200125Base
{
    void* m_pVtable;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int m_0c;

    static void* operator new(unsigned int size)
    {
        return FUN_00aa13e0(size);
    }

    C200125Object()
    {
        unsigned int count = 1;
        FUN_00c87c30();
        m_pVtable = &DAT_0102016c;
        m_0c = 0;
        DAT_01268154 += count;
        m_pVtable = &DAT_0102009c;
        DAT_01268118 += count;
        m_pVtable = &DAT_010c9634;
        DAT_012685b8 += count;
    }
};

struct C200125Owner
{
    void FUN_00c86800(C200125Object* object, unsigned int argument);
    C200125Object* FUN_00cc3540(unsigned int argument);
};

C200125Object* C200125Owner::FUN_00cc3540(unsigned int argument)
{
    TlsFlagGuard guard;
    FUN_00c876f0();

    C200125Object* object = new C200125Object;
    FUN_00c86800(object, argument);
    FUN_00c87700();
    return object;
}


