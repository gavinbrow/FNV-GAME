#include <xmmintrin.h>

struct FnvRayInput {
    __m128 from;
    __m128 to;
    float unk20;
    int fraction;
};
struct FnvTransform {
    __m128 axisX;
    __m128 axisY;
    __m128 axisZ;
    __m128 origin;
};
__declspec(align(16)) struct FnvQuery {
    FnvQuery() : fraction(0), filterScale(0) {}
    float startX, startY, startZ, startW;
    float endX, endY, endZ, endW;
    int fraction;
    void* filterScale;
};
struct FnvHit {
    __m128 position;
    float fraction;
    int unk14, unk18, unk1c, unk20, unk24, unk28, unk2c, unk30;
    int unk34, unk38, unk3c, unk40, unk44, unk48, unk4c;
    int* object;
};
struct FnvExistingHit {
    int unk00;
    float fraction;
};
struct FnvFilter {
    virtual void unused0();
    virtual unsigned char* accepts(unsigned char*, FnvRayInput*, int*);
};
struct FnvRayNode {
    virtual void unused0();
    virtual void unused1();
    virtual void unused2();
    virtual void unused3();
    virtual void unused4();
    virtual void unused5();
    virtual void unused6();
    virtual void unused7();
    virtual void collect(unsigned char*, FnvQuery*, FnvHit*);
    virtual void update(FnvQuery*, int*, FnvExistingHit*);
};

static __forceinline __m128 inversePoint(__m128 v, const FnvTransform* t) {
 __m128 d=_mm_sub_ps(v,t->origin); __m128 a=t->axisX,b=t->axisY,c=t->axisZ; __m128 low=_mm_unpacklo_ps(a,b),high=_mm_unpackhi_ps(a,b); a=_mm_movelh_ps(low,c); b=_mm_shuffle_ps(_mm_movehl_ps(a,low),c,0xd4); c=_mm_shuffle_ps(high,c,0xe4); __m128 y=_mm_mul_ps(b,_mm_shuffle_ps(d,d,0x55)); __m128 x=_mm_mul_ps(a,_mm_shuffle_ps(d,d,0)); __m128 z=_mm_mul_ps(c,_mm_shuffle_ps(d,d,0xaa)); return _mm_add_ps(_mm_add_ps(y,x),z);
}

struct FnvRaycasterState {
    int unk00;
    int unk04;
    FnvRayInput* ray;
    FnvFilter* filter;
    void* filterScale;
    FnvHit* hit;
    FnvExistingHit* existingHit;
    float fraction;
};

void hkpAabbTreeCollidableRaycaster::FUN_00d9a070(int request) {
    FnvRaycasterState* st = (FnvRaycasterState*)this;
    int* source = (int*)request;
    FnvRayNode* node = (FnvRayNode*)source[0];
    if (!node) return;
    unsigned char accepted;
    if (st->filter && !*st->filter->accepts(&accepted,st->ray,source)) return;
    FnvTransform* t = (FnvTransform*)source[2];
    FnvQuery query;
    _mm_store_ps(&query.startX,inversePoint(st->ray->from,t));
    _mm_store_ps(&query.endX,inversePoint(st->ray->to,t));
    query.fraction = st->ray->fraction;
    query.filterScale = st->filterScale;
    if (st->existingHit) {
        node->update(&query,source,st->existingHit);
        st->fraction = st->existingHit->fraction;
        return;
    }
    node->collect(&accepted,&query,st->hit);
    if (accepted) {
        st->hit->object = source;
        __m128 v = st->hit->position;
        __m128 y = _mm_mul_ps(_mm_shuffle_ps(v,v,0x55),t->axisY);
        __m128 x = _mm_mul_ps(_mm_shuffle_ps(v,v,0),t->axisX);
        __m128 z = _mm_mul_ps(_mm_shuffle_ps(v,v,0xaa),t->axisZ);
        st->hit->position = _mm_add_ps(_mm_add_ps(y,x),z);
        st->fraction = st->hit->fraction;
    }
}
