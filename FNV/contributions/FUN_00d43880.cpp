extern "C" void _ReadWriteBarrier(void);
#include <windows.h>

extern DWORD DAT_0126835c;

unsigned __int64 __cdecl __rdtsc(void);

struct ProfRec
{
    const char* m_pName;
    DWORD m_iTick;
    DWORD unk08;
};

struct ProfBuf
{
    DWORD unk00;
    ProfRec* m_pCur;
    DWORD unk08;
    ProfRec* m_pEnd;
};

struct ShapeResult
{
    DWORD m_ret;
    DWORD m_key;
    DWORD m_motion;
    void* m_parent;
};

struct ShapePair
{
    DWORD m_key;
    void* m_pObj;
};

__declspec(align(16)) struct ShapeKeyBuf
{
    DWORD m_key;
    DWORD unk04, unk08, unk0C, unk10, unk14, unk18, unk1C, unk20,
    unk24, unk28, unk2C, unk30, unk34, unk38, unk3C, unk40,
    unk44, unk48, unk4C, unk50, unk54, unk58, unk5C, unk60,
    unk64, unk68, unk6C, unk70, unk74, unk78, unk7C, unk80,
    unk84, unk88, unk8C, unk90, unk94, unk98, unk9C, unkA0,
    unkA4, unkA8, unkAC, unkB0, unkB4, unkB8, unkBC, unkC0,
    unkC4, unkC8, unkCC, unkD0, unkD4, unkD8, unkDC, unkE0,
    unkE4, unkE8, unkEC, unkF0, unkF4, unkF8, unkFC, unk100,
    unk104, unk108, unk10C, unk110, unk114, unk118, unk11C, unk120,
    unk124, unk128, unk12C, unk130, unk134, unk138, unk13C, unk140,
    unk144, unk148, unk14C, unk150, unk154, unk158, unk15C, unk160,
    unk164, unk168, unk16C, unk170, unk174, unk178, unk17C, unk180,
    unk184, unk188, unk18C, unk190, unk194, unk198, unk19C, unk1A0,
    unk1A4, unk1A8, unk1AC, unk1B0, unk1B4, unk1B8, unk1BC, unk1C0,
    unk1C4, unk1C8, unk1CC, unk1D0, unk1D4, unk1D8, unk1DC, unk1E0,
    unk1E4, unk1E8, unk1EC, unk1F0;
};

class ShapeSource
{
public:
    virtual void vtbl00(void);
    virtual void vtbl04(void);
    virtual void vtbl08(void);
    virtual void vtbl0C(void);
    virtual void* vtbl10(void);
};

class ShapeKeyHandler
{
public:
    virtual void vtbl00(void);
    virtual void vtbl04(void);
    virtual void vtbl08(void);
    virtual void vtbl0C(void);
    virtual void vtbl10(void);
    virtual DWORD vtbl14(DWORD key, ShapeKeyBuf* pOut);
};

class ShapeObject
{
public:
    virtual void vtbl00(void);
    virtual void vtbl04(void);
    virtual void vtbl08(void);
    virtual void vtbl0C(void);
    virtual void vtbl10(void* pKey, DWORD a1, DWORD a2, DWORD a3);
};

struct ShapeHolder
{
    ShapeSource* m_pSrc;
    DWORD unk04;
    DWORD m_dw08;
};

struct FUN_00d43880_cls : public hkpShapeCollectionAgent
{
    void FUN_00d43880(ShapeHolder* pHolder, DWORD a1, DWORD a2, DWORD a3);
};

void FUN_00d43880_cls::FUN_00d43880(ShapeHolder* pHolder, DWORD a1, DWORD a2, DWORD a3)
{
    ProfBuf* pBuf = (ProfBuf*)TlsGetValue(DAT_0126835c);
    if (pBuf->m_pCur < pBuf->m_pEnd)
    {
        ProfRec* pRec = pBuf->m_pCur;
        pRec->m_pName = "TtShapeCollection";
        _ReadWriteBarrier();
        volatile DWORD tick = (DWORD)__rdtsc();
        pRec->m_iTick = tick;
        pBuf->m_pCur = pRec + 1;
    }

    ShapeKeyHandler* pHandler = (ShapeKeyHandler*)pHolder->m_pSrc->vtbl10();
    ShapeResult res;
    res.m_motion = pHolder->m_dw08;
    int i = this->count - 1;
    res.m_parent = pHolder;
    ShapePair* pPair = (ShapePair*)this->p2;
    ShapeKeyBuf keyBuf;
    if (i >= 0)
    {
        do
        {
            DWORD key = pPair->m_key;
            res.m_ret = pHandler->vtbl14(key, &keyBuf);
            res.m_key = key;
            ShapeObject* pObj = (ShapeObject*)pPair->m_pObj;
            pObj->vtbl10(&res, a1, a2, a3);
            pPair++;
            i--;
        } while (i >= 0);
    }

    pBuf = (ProfBuf*)TlsGetValue(DAT_0126835c);
    if (pBuf->m_pCur < pBuf->m_pEnd)
    {
        ProfRec* pRec = pBuf->m_pCur;
        pRec->m_pName = "Et";
        _ReadWriteBarrier();
        volatile DWORD tick = (DWORD)__rdtsc();
        pRec->m_iTick = tick;
        pBuf->m_pCur = pRec + 1;
    }
}
