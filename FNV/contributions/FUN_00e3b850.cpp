#include <xmmintrin.h>
struct Motor { void FUN_00c90510(); };
struct ConstraintInfo {
    __m128 frameA;
    __m128 frameB;
    __m128 frameC;
    __m128 frameD;
    Motor* motorA;
    Motor* motorB;
    Motor* motorC;
    bool enabled;
};
struct InfoArray {
    ConstraintInfo* data;
    int size;
    unsigned int capacityAndFlags;
};
struct MemoryRouter {
    int unk00, unk04, unk08, unk0c;
    void* allocator;
};
extern void __cdecl FUN_00c90940(void* allocator, InfoArray* array, int elementSize);
extern const __m128 DAT_012683b0;
struct PoweredChainData {
    int unk00, unk04, unk08, unk0c, unk10, unk14;
    InfoArray infos;
    MemoryRouter* FUN_00c85750();
    void FUN_00e3b850(const __m128* a, const __m128* b, const __m128* c,
                       Motor* motorA, Motor* motorB, Motor* motorC);
};
void PoweredChainData::FUN_00e3b850(const __m128* a, const __m128* b, const __m128* c,
                                    Motor* motorA, Motor* motorB, Motor* motorC) {
    InfoArray* array = &infos;
    MemoryRouter* router = FUN_00c85750();
    if (array->size == (int)(array->capacityAndFlags & 0x3fffffff))
        FUN_00c90940(router->allocator, array, sizeof(ConstraintInfo));
    ConstraintInfo& info = array->data[array->size++];
    info.frameA = *a;
    info.frameB = *b;
    info.frameC = *c;
    info.motorA = motorA;
    motorA->FUN_00c90510();
    info.motorB = motorB;
    motorB->FUN_00c90510();
    info.motorC = motorC;
    motorC->FUN_00c90510();
    info.enabled = false;
    info.frameD = DAT_012683b0;
}