#include <xmmintrin.h>
struct FNVAction {
    const void* vtable;
    unsigned short memoryFlags;
    short referenceCount;
    void* world;
    void* island;
    unsigned int userData;
    const char* name;
    void* entity;
    void FUN_00d2b260(void* entity, unsigned int option);
};
extern int DAT_010e6834;
struct FUN_00e444f0 : FNVAction {
    int unk1c;
    __m128 rotationAxis;
    __m128 upAxis;
    float strength;
    float damping;
    FUN_00e444f0(void* entity, const __m128* rotation, const __m128* up, float strengthValue, float dampingValue);
};
FUN_00e444f0::FUN_00e444f0(void* e, const __m128* r, const __m128* u, float s, float d) {
    FUN_00d2b260(e, 0);
    vtable = &DAT_010e6834;
    rotationAxis = *r;
    upAxis = *u;
    strength = s;
    damping = d;
}