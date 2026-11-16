#include "h_74712c1d3c73.h"

struct FUN_00a26520_Class {
    void FUN_00a26520(int a, short* b, int c);
};

void __stdcall FUN_00ee820a(int a, short* b);

struct TwoShorts {
    short x;
    short y;
};

void FUN_00a269f0_Class::FUN_00a269f0(int a) {
    if (a >= 1) {
        TwoShorts s = {0, 0};
        ((FUN_00a26520_Class*)this)->FUN_00a26520(0, &s.x, a);
        ((FUN_00a26520_Class*)this)->FUN_00a26520(1, &s.x, a);
        FUN_00ee820a(*(int*)this, &s.x);
    }
}
