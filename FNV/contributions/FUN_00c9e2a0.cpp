#include <xmmintrin.h>

struct __declspec(align(16)) Vec4
{
    float x, y, z, w;
};

struct Mat3
{
    Vec4 c0, c1, c2;
};

struct Out
{
    Vec4 v;
    float t;
    int flags;
    int unk01;
    int unk02;
    int b;
    int unk03;
    int unk04;
    int unk05;
    int unk06;
    int unk07;
    int unk08;
    int unk09;
    int c;
};

struct P2
{
    int unk0;
    int unk1;
    Mat3 *m;
};

struct Cb;

struct VTable
{
    void (__thiscall *fn)(Cb *, P2 *, Vec4 *);
};

struct Cb
{
    VTable *vt;
    float f;
};

class Shape
{
public:
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual void v4();
    virtual void v5();
    virtual void v6();
    virtual void v7();
    virtual void v8(bool *ok, void *p1, Out *out);
};

struct FN : public Shape
{
    void FUN_00c9e2a0(int p1, int p2, Cb *p3);
};

void FN::FUN_00c9e2a0(int p1, int p2, Cb *p3)
{
    bool ok;
    Out out;

    out.t = p3->f;
    out.flags = -1;
    out.b = -1;
    out.c = 0;

    this->v8(&ok, (void *)(*(volatile int *)&p1), &out);

    if (ok)
    {
        __m128 v = _mm_load_ps(&out.v.x);
        int p2Value = p2;
        P2 *q = (P2 *)p2Value;
        Mat3 *m = q->m;
        VTable *vt = p3->vt;
        void (__thiscall *fn)(Cb *, P2 *, Vec4 *) = vt->fn;

        __m128 c0 = _mm_load_ps(&m->c0.x);
        __m128 c1 = _mm_load_ps(&m->c1.x);
        __m128 c2 = _mm_load_ps(&m->c2.x);

        __m128 r = _mm_add_ps(
            _mm_mul_ps(_mm_shuffle_ps(v, v, 0x55), c1),
            _mm_mul_ps(_mm_shuffle_ps(v, v, 0), c0));
        r = _mm_add_ps(r, _mm_mul_ps(_mm_shuffle_ps(v, v, 0xaa), c2));

        _mm_store_ps(&out.v.x, r);
        fn(p3, q, &out.v);
    }
}
