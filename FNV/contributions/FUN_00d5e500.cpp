extern "C" void _ReadWriteBarrier(void);
#include <windows.h>

extern DWORD DAT_0126835c;
unsigned __int64 __cdecl __rdtsc(void);

struct ProfRec { const char* m_pName; DWORD m_iTick; DWORD unk08; };
struct ProfBuf { DWORD unk00; ProfRec* m_pCur; DWORD unk08; ProfRec* m_pEnd; };

struct Node;
struct Coll {
    virtual void v00();
    virtual void v04();
    virtual int First();
    virtual int Next(int id);
    virtual void v10();
    virtual Node* Get(int id, void* buf);
};
struct State {
    DWORD unk00, unk04, unk08, unk0C, unk10, unk14, unk18, unk1C;
    int slots[8];
    int depth;
};
struct Node {
    virtual void v00(); virtual void v04(); virtual void v08(); virtual void v0C();
    virtual void v10(); virtual void v14(); virtual void v18(); virtual void v1C();
    virtual bool* FUN_00d5e500(bool* __restrict result, void* other, State* st);
    DWORD unk04, unk08, unk0C, unk10;
    Coll coll;
};
struct __declspec(align(16)) Buf { DWORD d[128]; };

bool* Node::FUN_00d5e500(bool* __restrict result, void* other, State* st)
{
    Buf buf;
    struct F { bool a, b, c, d; } fnd;
    ProfBuf* pBuf = (ProfBuf*)TlsGetValue(DAT_0126835c);
    if (pBuf->m_pCur < pBuf->m_pEnd) {
        ProfRec* pRec = pBuf->m_pCur;
        volatile DWORD ticks;
        pRec->m_pName = "TtrcCxList";
        _ReadWriteBarrier();
        ticks = (DWORD)__rdtsc();
        pRec->m_iTick = ticks;
        pBuf->m_pCur = pRec + 1;
    }
    st->depth++;
    int sel = -1;
    for (int id = coll.First(); id != -1; id = coll.Next(id)) {
        coll.Get(id, &buf)->FUN_00d5e500(&fnd.d, other, st);
        if (fnd.d) sel = id;
    }
    st->depth--;
    if (sel != -1) st->slots[st->depth] = sel;
    *result = sel != -1;
    pBuf = (ProfBuf*)TlsGetValue(DAT_0126835c);
    if (pBuf->m_pCur < pBuf->m_pEnd) {
        ProfRec* pRec = pBuf->m_pCur;
        volatile DWORD ticks;
        pRec->m_pName = "Et";
        _ReadWriteBarrier();
        ticks = (DWORD)__rdtsc();
        pRec->m_iTick = ticks;
        pBuf->m_pCur = pRec + 1;
    }
    return result;
}
