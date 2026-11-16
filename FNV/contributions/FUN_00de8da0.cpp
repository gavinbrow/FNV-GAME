#include <xmmintrin.h>

struct __declspec(align(16)) Vector4
{
    float x;
    float y;
    float z;
    float w;
};

struct Matrix4;
struct MatrixPointer
{
    const Matrix4* volatile value;
    MatrixPointer(const MatrixPointer& other);
};

struct Matrix4
{
    Vector4 row0;
    Vector4 row1;
    Vector4 row2;
    Vector4 row3;

    Matrix4(const Matrix4& value)
    {
        _mm_store_ps(&row0.x, _mm_load_ps(&value.row0.x));
        _mm_store_ps(&row1.x, _mm_load_ps(&value.row1.x));
        _mm_store_ps(&row2.x, _mm_load_ps(&value.row2.x));
        _mm_store_ps(&row3.x, _mm_load_ps(&value.row3.x));
    }

    __declspec(noinline) void __fastcall FUN_00de87c0(Matrix4* context);
    void FUN_00de8da0(const Matrix4* left, MatrixPointer right);
};

void __fastcall Matrix4::FUN_00de87c0(Matrix4* context)
{
    __m128* vectors = reinterpret_cast<__m128*>(this);
    __m128 low01 = _mm_unpacklo_ps(vectors[0], vectors[1]);
    __m128 high01 = _mm_unpackhi_ps(vectors[0], vectors[1]);
    __m128 low23 = _mm_unpacklo_ps(vectors[2], vectors[3]);
    __m128 high23 = _mm_unpackhi_ps(vectors[2], vectors[3]);
    vectors[0] = _mm_movelh_ps(low01, low23);
    vectors[1] = _mm_movehl_ps(low23, low01);
    vectors[2] = _mm_movelh_ps(high01, high23);
    vectors[3] = _mm_movehl_ps(high23, high01);
}

__forceinline float Dot4(const float* left, const float* right)
{
    __m128 first = *reinterpret_cast<const __m128*>(left);
    __m128 second = *reinterpret_cast<const __m128*>(right);
    __m128 product = _mm_mul_ps(first, second);
    __m128 halves = _mm_add_ps(_mm_shuffle_ps(product, product, 0x4e), product);
    __m128 sum = _mm_add_ps(_mm_shuffle_ps(halves, halves, 0xb1), halves);
    float scalar;
    _mm_store_ss(&scalar, sum);
    return scalar;
}

void Matrix4::FUN_00de8da0(const Matrix4* left, MatrixPointer right)
{
    Matrix4 columns(*left);
    columns.FUN_00de87c0(this);
    float* destination = reinterpret_cast<float*>(this);
    const float* input = reinterpret_cast<const float*>(right.value);
    for (int row = 0; row != 4; ++row)
    {
        for (int column = 0; column != 4; ++column)
        {
            destination[row * 4 + column] = Dot4(
                input + row * 4,
                reinterpret_cast<const float*>(&columns) + column * 4);
        }
    }
}
