struct FUN_00acd060_buf
{
    volatile unsigned int m_cursor;
};

struct FUN_00acd060_cls
{
    virtual void vfn00();
    virtual void vfn01();
    virtual void vfn02(int value);
    virtual void vfn03();
    virtual void vfn04();
    virtual int vfn05();

    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1C;
    FUN_00acd060_buf* m_pBuf;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2C;
    unsigned int* m_pLimit;

    int FUN_00acd060();
};

int FUN_00acd060_cls::FUN_00acd060()
{
    unsigned int q2 = m_pBuf->m_cursor;
    unsigned int q1;
    int res;
    int m1;

    if ((q2 != 0) && ((q1 = m_pBuf->m_cursor) < *m_pLimit + m_pBuf->m_cursor))
    {
        unsigned int q3 = m_pBuf->m_cursor;
        return *(unsigned char*)q3;
    }
    else
    {
        res = vfn05();
        m1 = -1;
        if ((unsigned char)(unsigned short)(m1 == res))
        {
            return res;
        }
        else
        {
            vfn02(res);
            return res;
        }
    }
}