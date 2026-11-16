
struct WeightedVertex {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    __m128 position;
};

struct VertexTriple {
    unsigned int unk00;
    unsigned int unk04;
    WeightedVertex* first;
    WeightedVertex* second;
    WeightedVertex* third;
};

struct FUN_00e21ed0_Class {
    unsigned int unk00;
    VertexTriple* vertices;
    void FUN_00e21ed0(const __m128* direction, __m128* output);
};

static __forceinline __m128 Dot3(__m128 product)
{
    __m128 xy = _mm_add_ss(_mm_shuffle_ps(product, product, 0x55), product);
    return _mm_add_ss(_mm_shuffle_ps(product, product, 0xaa), xy);
}
static __forceinline float Scalar(__m128 value)
{
    float result;
    _mm_store_ss(&result, value);
    return result;
}

void FUN_00e21ed0_Class::FUN_00e21ed0(const __m128* direction, __m128* output)
{
    VertexTriple* set = vertices;
    WeightedVertex* a = set->first;
    WeightedVertex* b = set->second;
    WeightedVertex* c = set->third;
    __m128 vector = *direction;

    __m128 scoreA = Dot3(_mm_mul_ps(a->position, vector));
    __m128 scoreB = Dot3(_mm_mul_ps(b->position, vector));
    __m128 scoreC = Dot3(_mm_mul_ps(c->position, vector));

    unsigned int selected;
    if (Scalar(scoreA) > Scalar(scoreB))
        selected = Scalar(scoreA) > Scalar(scoreC) ? 0 : 2;
    else
        selected = Scalar(scoreB) > Scalar(scoreC) ? 1 : 2;

    WeightedVertex* chosen = (&set->first)[selected];
    *output = chosen->position;
    reinterpret_cast<unsigned int*>(output)[3] = 0x3f000000u | selected;
}
