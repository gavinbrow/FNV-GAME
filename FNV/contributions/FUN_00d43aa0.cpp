#include <windows.h>
#include <intrin.h>

extern DWORD g_tlsIndex;

struct Rec {
    const char* name;
    unsigned int ticks;
    int unk08;
};

struct ProfilerBuf {
    int unk00;
    Rec* cur;
    int unk08;
    Rec* end;
};

struct Queryable {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0c();
    virtual void v10();
    virtual int v14(int id, void* out);
};

struct Source {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0c();
    virtual Queryable* v10();
};

struct Holder {
    Source* unk00;
    int unk04;
    int unk08;
};

struct Packet {
    int result;
    int id;
    int unk08;
    Holder* holder;
};

struct Handler {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0c();
    virtual void v10();
    virtual void v14(Packet* packet, int a, int b, int c, int d);
};

struct Pair {
    int id;
    Handler* handler;
};

struct __declspec(align(16)) B16 { int a; int b; int c; int d; };
struct B64 { B16 a; B16 b; B16 c; B16 d; };
struct B256 { B64 a; B64 b; B64 c; B64 d; };
struct B512 { B256 a; B256 b; };

// Calling convention note: declared __thiscall as in the packet (this in ecx, callee pops 20 bytes).
struct Agent : hkpShapeCollectionAgent {
    void FUN_00d43aa0(Holder* holder, int a, int b, int c, int d);
};

void Agent::FUN_00d43aa0(Holder* holder, int a, int b, int c, int d)
{
    ProfilerBuf* pb = (ProfilerBuf*)TlsGetValue(g_tlsIndex);
    Rec* cur = pb->cur;
    if (cur < pb->end) {
        volatile unsigned int t;
        cur->name = "TtShapeCollection";
        _ReadWriteBarrier();
        t = (unsigned int)__rdtsc();
        cur->ticks = t;
        pb->cur = cur + 1;
    }
    Queryable* q = holder->unk00->v10();
    Packet packet;
    B512 buf;
    packet.unk08 = holder->unk08;
    packet.holder = holder;
    Pair* p = (Pair*)p2;
    for (int i = count - 1; i >= 0; i--) {
        int id = p->id;
        int r = q->v14(id, &buf);
        packet.result = r;
        packet.id = id;
        p->handler->v14(&packet, a, b, c, d);
        p++;
    }
    pb = (ProfilerBuf*)TlsGetValue(g_tlsIndex);
    cur = pb->cur;
    if (cur < pb->end) {
        volatile unsigned int t;
        cur->name = "Et";
        _ReadWriteBarrier();
        t = (unsigned int)__rdtsc();
        cur->ticks = t;
        pb->cur = cur + 1;
    }
}
