extern "C" void _ReadWriteBarrier(void);
#include <windows.h>
extern DWORD DAT_0126835c;
unsigned __int64 __cdecl __rdtsc(void);
struct ProfRec { const char* m_pName; DWORD m_iTick; DWORD unk08; };
struct ProfBuf { DWORD unk00; ProfRec* m_pCur; DWORD unk08; ProfRec* m_pEnd; };
struct Inner {
    DWORD unk00, unk04, unk08, unk0C, unk10, unk14, unk18, unk1C;
    int m_20; int m_24; int m_28;
};
struct Frame {
    DWORD unk00, unk04, unk08, unk0C, unk10, unk14, unk18, unk1C;
    int m_20; int m_24; int m_28; Inner* m_2C; int m_30;
};
class Target { public: void FUN_00d04e80(void* a, void* b, int c); };
int FUN_00d1d540(int a, Inner* b, int* c, int d);
int FUN_00d1d4d0(int a, Inner* b, int* c, int d);
int FUN_00d1b930(int a, Inner* b, int* c, int d);
void __cdecl FUN_00df6850(Target* self, Frame* p)
{
    ProfBuf* pBuf = (ProfBuf*)TlsGetValue(DAT_0126835c);
    if (pBuf->m_pCur < pBuf->m_pEnd) {
        ProfRec* pRec = pBuf->m_pCur;
        pRec->m_pName = "TtCpuAabbTreeAabb";
        _ReadWriteBarrier();
        volatile DWORD tick = (DWORD)__rdtsc();
        pRec->m_iTick = tick;
        pBuf->m_pCur = pRec + 1;
    }
    Frame* fr = p;
    int* rem = (int*)(&self + 1);
    Inner* in = fr->m_2C;
    int n = fr->m_30;
    if (n > 0) {
        int k = n;
        do {
            int cnt = in->m_20;
            int initial = in->m_24;
            in->m_28 = 0;
            *rem = initial;
            if (fr->m_20) { int r = FUN_00d1d540(fr->m_20, in, rem, cnt); in->m_28 += r; cnt -= r; }
            if (fr->m_24) { int r = FUN_00d1d4d0(fr->m_24, in, rem, cnt); in->m_28 += r; cnt -= r; }
            if (fr->m_28) { int r = FUN_00d1b930(fr->m_28, in, rem, cnt); in->m_28 += r; }
            in = (Inner*)((char*)in + 0x30);
        } while (--k);
    }
    pBuf = (ProfBuf*)TlsGetValue(DAT_0126835c);
    if (pBuf->m_pCur < pBuf->m_pEnd) {
        ProfRec* pRec = pBuf->m_pCur;
        pRec->m_pName = "Et";
        _ReadWriteBarrier();
        volatile DWORD t2 = (DWORD)__rdtsc();
        pRec->m_iTick = t2;
        pBuf->m_pCur = pRec + 1;
    }
    self->FUN_00d04e80(fr, fr, 0);
}
