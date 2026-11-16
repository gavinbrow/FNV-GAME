union __declspec(intrin_type) __declspec(align(16)) __m128 { float m128_f32[4]; unsigned __int64 m128_u64[2]; };
extern "C" __m128 _mm_sub_ps(__m128, __m128);
extern "C" __m128 _mm_add_ps(__m128, __m128);
extern "C" __m128 _mm_shuffle_ps(__m128, __m128, unsigned int);
extern "C" __m128 _mm_unpackhi_ps(__m128, __m128);
extern "C" __m128 _mm_setzero_ps();
extern "C" __m128 _mm_set_ps1(float);
extern "C" double DAT_01091c00;
extern "C" __m128 _mm_load_ss(const float*);
union __declspec(align(16)) QueryVector {
    __m128 quad;
    struct { float x, y, z, w; } components;
};
struct QueryCode {
    int unk00, unk04, unk08, unk0c;
    QueryVector offset;
    unsigned char* data;
};
struct QueryState {
    int primitiveOffset, properties, x, y, z, shift;
    QueryState() { x=0; y=0; z=0; primitiveOffset=0; properties=0; }
};
struct QueryBounds { QueryVector low, high; };
struct SphereQuery {
    void* hits;
    int unk04, unk08, unk0c;
    float inverseScale;
    int unk14, unk18, unk1c;
    void* volatile collector;
    int unk24, unk28, unk2c;
    QueryVector sphere;
    void FUN_00e5fb50(QueryState*, unsigned char*, QueryBounds*);
};
void __cdecl FUN_00e5d710(const QueryCode* __restrict code, const QueryVector* sphere, void* hits, void* collector)
{
    SphereQuery query;
    QueryBounds bounds;
    query.inverseScale = 1.0f / code->offset.components.w;
    query.hits = hits;
    unsigned char* __restrict data = code->data;
    __m128 offset = code->offset.quad;
    bounds.low.quad = _mm_setzero_ps();
    QueryState state;
    float scaled = (float)(query.inverseScale * DAT_01091c00);
    bounds.high.quad = _mm_set_ps1(scaled);
    __m128 delta = _mm_sub_ps(sphere->quad, offset);
    delta = _mm_add_ps(delta, delta);
    query.sphere.quad = _mm_shuffle_ps(delta, _mm_unpackhi_ps(delta, query.sphere.quad), 0xc4);
    query.sphere.components.w = sphere->components.w + sphere->components.w;
    query.collector = collector;
    state.shift = 16;
    query.FUN_00e5fb50(&state, data, &bounds);
}
