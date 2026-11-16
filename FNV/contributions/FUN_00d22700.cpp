#include <xmmintrin.h>

struct __declspec(align(16)) Point4 {
    float x, y, z, w;
};
struct ClosestLineResult {
    float distance;
    float fractionA;
    float fractionB;
    float extraValue;
    Point4 pointA;
    Point4 pointB;
};
void __cdecl FUN_00d231b0(const Point4& a, const Point4& b,
                            const Point4& c, const Point4& d,
                            ClosestLineResult* out);
void __cdecl FUN_00d22700(const Point4& a, const Point4& b,
                           const Point4& c, const Point4& d,
                           float* distance, float* fractionA, float* fractionB,
                           Point4* pointA, Point4* pointB)
{
    ClosestLineResult result;
    FUN_00d231b0(a, b, c, d, &result);
    *reinterpret_cast<__m128*>(pointA) = *reinterpret_cast<const __m128*>(&result.pointA);
    *reinterpret_cast<__m128*>(pointB) = *reinterpret_cast<const __m128*>(&result.pointB);
    *fractionA = result.fractionA;
    *fractionB = result.fractionB;
    *distance = result.distance;
}
