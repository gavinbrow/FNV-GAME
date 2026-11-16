#include <xmmintrin.h>
class SphereMotionFacade {
public:
    void FUN_00d1e3d0(hkMatrix3* out);
};
void SphereMotionFacade::FUN_00d1e3d0(hkMatrix3* out) {
    float inverse = *(float*)((char*)this + 0xc0);
    __m128 zero = _mm_setzero_ps();
    __m128* columns = reinterpret_cast<__m128*>(out);
    columns[0] = zero;
    columns[1] = zero;
    columns[2] = zero;
    volatile float* diag = reinterpret_cast<volatile float*>(out);
    diag[0] = inverse;
    diag[5] = inverse;
    diag[10] = inverse;
}
