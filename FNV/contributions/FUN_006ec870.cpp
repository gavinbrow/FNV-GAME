struct FUN_006ec870 : InterfacedClass {
    int* m_pSlots;
    unsigned int m_uiBuckets;
    CF_0081c630* m_pBuckets;
    int m_iParam;

    void __thiscall FUN_0044c480(int value);
    ~FUN_006ec870();
};

FUN_006ec870::~FUN_006ec870()
{
    FUN_0044c480(1);
    delete m_pBuckets;
    delete m_pSlots;
}
