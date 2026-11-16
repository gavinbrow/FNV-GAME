extern int DAT_010c6fd0;
extern int DAT_010ce404;

struct CC9F10Shape {
    void FUN_00c90510();
};

struct FUN_00d26b50 {
    const int* m_pVT;
    char pad4[2];
    unsigned short m_uiFlags;
    int m_iA;
    int m_iB;
    unsigned char m_bC;
    char pad11[3];
    const int* m_pD;
    CC9F10Shape* m_pShape;
    char pad1d[4];
    unsigned char m_bE;
    FUN_00d26b50(CC9F10Shape* pShape, unsigned char bE);
};

FUN_00d26b50::FUN_00d26b50(CC9F10Shape* pShape, unsigned char bE)
{
    m_uiFlags = 1;
    m_iA = 0;
    m_iB = 8;
    m_bC = 1;
    m_pVT = &DAT_010ce404;
    m_pD = &DAT_010c6fd0;
    m_pShape = pShape;
    m_pShape->FUN_00c90510();
    m_bE = bE;
}