#include <xmmintrin.h>

struct Row {
    union {
        __m128 v;
        float f0;
    };
};

struct Matrix {
    Row r0;
    Row r1;
    Row r2;
    Row r3;
};

struct Obj : Matrix {
    void __thiscall FUN_00cb2240(Matrix* m, int a);
    void __thiscall FUN_00cb23e0(int a);
};

void __thiscall Obj::FUN_00cb23e0(int a)
{
    Matrix copy;
    copy.r0.v = r0.v;
    copy.r1.v = r1.v;
    copy.r2.v = r2.v;
    copy.r3.v = r3.v;
    FUN_00cb2240(&copy, a);
}
