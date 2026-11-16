#include <xmmintrin.h>
struct FUN_00cf0820 {
    float field00;
    float field04;
    unsigned int unk08;
    unsigned int unk0c;
    __m128 field10;
    __m128 field20;
    __m128 field30;
    __m128 field40;
    FUN_00cf0820(const FUN_00cf0820& input);
};
FUN_00cf0820::FUN_00cf0820(const FUN_00cf0820& input) {
    field00 = input.field00;
    field04 = input.field04;
    field10 = input.field10;
    field20 = input.field20;
    field30 = input.field30;
    field40 = input.field40;
}