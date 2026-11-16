#include <xmmintrin.h>

extern float DAT_0104da48;
extern unsigned int DAT_010c44d0;
extern unsigned int DAT_010ce80c;

struct Head50 {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    int unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    int unk40, unk44, unk48, unk4c;
};

struct Quad {
    int x, y, z, w;
};

struct Tail10 {
    int unk00, unk04, unk08, unk0c;
};

struct QueryCtx {
    Head50 head;
    Quad vec;
    Tail10 tail;
};

struct Handle {
    int value;
};

__declspec(align(16)) struct QueryObj {
    const void* vtable;
    float scale;
    int unk08;
    int unk0c;
    Quad vec;
    int extra;
    void Init(const Quad& v, int e)
    {
        vtable = &DAT_010ce80c;
        scale = DAT_0104da48;
        vec = v;
        extra = e;
    }
};

struct FUN_00d2dd70_class {
    void __thiscall FUN_00d2dd70(Handle a, Handle b, void* c, void* d, void* e);
    void __thiscall FUN_00d2ef30(Handle p1, Handle p2, QueryCtx* ctx, int e1, int e2);
};

void __thiscall FUN_00d2dd70_class::FUN_00d2ef30(Handle p1, Handle p2, QueryCtx* ctx, int e1, int e2)
{
    QueryObj q2;
    QueryObj q1;
    float s = DAT_0104da48;
    __m128 v = *(const __m128*)&ctx->vec;
    q1.scale = s;
    __m128 neg = _mm_xor_ps(v, *(const __m128*)&DAT_010c44d0);
    QueryCtx local = *ctx;
    *(__m128*)&local.vec = neg;
    q1.vec = ctx->vec;
    q1.extra = e1;
    q1.vtable = &DAT_010ce80c;
    if (e2) {
        q2.Init(ctx->vec, e2);
        FUN_00d2dd70(p2, p1, &local, &q1, &q2);
    } else {
        FUN_00d2dd70(p2, p1, &local, &q1, 0);
    }
}
