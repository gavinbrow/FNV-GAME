#include <xmmintrin.h>
struct SRC{int m_00,m_04,m_08,m_0c;float m_10,m_14,m_18,m_1c;__m128 m_20;};
struct DST{int m_00,m_04,m_08,m_0c,m_10,m_14,m_18,m_1c,m_20,m_24,m_28,m_2c;float m_30;};
struct VEC{float q[4];void FUN_00a38560();void FUN_004f0180(void*);};
void* __cdecl FUN_00458620(void*,const void*);
struct LOC{float s;char quat[16];}; DST* __cdecl FUN_00c74d50(DST* dst,const SRC* src){LOC a;VEC* q=(VEC*)&a.quat;q->q[1]=src->m_10;q->q[2]=src->m_14;q->q[3]=src->m_18;q->q[0]=src->m_1c;q->FUN_00a38560();q->FUN_004f0180(dst);FUN_00458620(&dst->m_24,src);_mm_store_ss(&a.s,src->m_20);dst->m_30=a.s;return dst;}