extern "C" unsigned __int64 __rdtsc(void);
extern "C" void _ReadWriteBarrier(void);
extern "C" __declspec(dllimport) void* __stdcall TlsGetValue(unsigned long);
extern unsigned long DAT_0126835c;
extern char DAT_010cebd0;

struct MonStream { int unk00; char* m_end; int unk08; char* m_capacity; };
struct MonEntry { const char* name; unsigned int ticks; int unk08; };
struct MonEntryObj { const char* name; unsigned int ticks; int unk08; const char* obj; };

inline void TimerBeginObj(const char* name, const char* obj)
{
    MonStream* ms = (MonStream*)TlsGetValue(DAT_0126835c);
    MonEntryObj* p = (MonEntryObj*)ms->m_end;
    if ((char*)p < ms->m_capacity) {
        p->name = name;
        p->obj = obj;
        _ReadWriteBarrier();
        volatile unsigned int t = (unsigned int)__rdtsc();
        p->ticks = t;
        ms->m_end = (char*)(p + 1);
    }
}
inline void TimerMark(const char* name)
{
    MonStream* ms = (MonStream*)TlsGetValue(DAT_0126835c);
    MonEntry* p = (MonEntry*)ms->m_end;
    if ((char*)p < ms->m_capacity) {
        p->name = name;
        _ReadWriteBarrier();
        volatile unsigned int t = (unsigned int)__rdtsc();
        p->ticks = t;
        ms->m_end = (char*)(p + 1);
    }
}

extern char DAT_010cf414[];
extern char DAT_010cf404[];
extern char DAT_010cec4c[];
extern char DAT_01076f38[];

struct BvShape {
  int unk00, unk04, unk08;
  unsigned int m_type;
  BvShape* m_boundingShape;
  int unk14;
  BvShape* m_childShape;
};
struct CdBody {
  BvShape* m_shape;
  unsigned int m_key;
  unsigned int m_motion;
  CdBody* m_parent;
};
struct CollisionInput;
typedef void (__cdecl *CollideFn)(CdBody* a, CdBody* b, CollisionInput* input, void* collector);
struct DispatchEntry {
  CollideFn m_fn0;
  CollideFn m_fn1;
  int unk08, unk0c, unk10;
};
struct CollisionInput { unsigned char* m_dispatcher; };
struct EarlyOutCollector { void* m_vtbl; bool m_hit; };
union BeginRecordOrCollector {
    volatile unsigned int tick;
    EarlyOutCollector early;
};

void __cdecl FUN_00d45af0(CdBody* bodyA, CdBody* bodyB, CollisionInput* input, void* collector)
{
    CdBody child;
    BeginRecordOrCollector scratch;
    {
        MonStream* ms = (MonStream*)TlsGetValue(DAT_0126835c);
        MonEntryObj* p = (MonEntryObj*)ms->m_end;
        if ((char*)p < ms->m_capacity) {
            p->name = DAT_010cf414;
            p->obj = DAT_010cf404;
            _ReadWriteBarrier();
            scratch.tick = (unsigned int)__rdtsc();
            p->ticks = scratch.tick;
            ms->m_end = (char*)(p + 1);
        }
    }
    BvShape* bv = bodyA->m_shape;
    child.m_parent = bodyA;
    child.m_motion = bodyA->m_motion;
    child.m_shape = bv->m_boundingShape;
    child.m_key = 0xffffffff;
    unsigned int typeB = bodyB->m_shape->m_type;
    unsigned char* table = input->m_dispatcher;
    DispatchEntry* entries = (DispatchEntry*)(table + 0x9a4);
    CollideFn firstHandler = entries[table[(child.m_shape->m_type + 13) * 32 + typeB]].m_fn0;
    scratch.early.m_vtbl = &DAT_010cebd0;
    scratch.early.m_hit = false;
    firstHandler(&child, bodyB, input, &scratch.early);
    if (scratch.early.m_hit) {
        TimerMark(DAT_010cec4c);
        child.m_shape = bv->m_childShape;
        child.m_key = 0;
        table = input->m_dispatcher;
        entries = (DispatchEntry*)(table + 0x9a4);
        entries[table[(child.m_shape->m_type + 13) * 32 + typeB]].m_fn1(&child, bodyB, input, collector);
    }
    TimerMark(DAT_01076f38);
}