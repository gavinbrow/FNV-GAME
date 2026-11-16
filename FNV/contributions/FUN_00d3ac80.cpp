#include <xmmintrin.h>

struct __declspec(align(16)) FourWord {
    unsigned int x, y, z, w;
};

struct __declspec(align(16)) FourFloat {
    union { __m128 simd; FourWord words; };
};

struct __declspec(align(16)) MotionPacket {
    unsigned int word00;
    unsigned int word04;
    unsigned int word08;
    unsigned int word0c;
    unsigned int word10;
    unsigned int word14;
    unsigned int word18;
    unsigned int word1c;
    unsigned int word20;
    unsigned int word24;
    unsigned int word28;
    unsigned int word2c;
    unsigned int word30;
    unsigned int word34;
    unsigned int word38;
    unsigned int word3c;
    unsigned int word40;
    unsigned int word44;
    unsigned int word48;
    unsigned int word4c;
    FourFloat direction;
    unsigned int trailing60, trailing64, trailing68, trailing6c;
};

struct __declspec(align(16)) MotionCallData {
    const void* descriptor;
    float scale;
    FourWord direction;
    unsigned int mode;
};

extern "C" float DAT_0104da48;
extern "C" const __m128 DAT_010c44d0;
extern "C" unsigned char UNK_010ce80c;

extern "C" void __cdecl FUN_00daf8e0(unsigned int second, unsigned int first,
                            MotionPacket* packet, MotionCallData* primary,
                            MotionCallData* secondary);

void __cdecl FUN_00d3ac80(unsigned int first, unsigned int second,
                           const MotionPacket* input, unsigned int mode,
                           unsigned int optionalMode)
{
    MotionPacket modified = *input;
    modified.direction.simd = _mm_xor_ps(input->direction.simd, DAT_010c44d0);
    const void* descriptor = &UNK_010ce80c;
    MotionCallData primary;
    primary.descriptor = descriptor;
    primary.scale = DAT_0104da48;
    primary.direction = input->direction.words;
    primary.mode = mode;

    if (optionalMode) {
        MotionCallData secondary;
        secondary.descriptor = descriptor;
        secondary.scale = DAT_0104da48;
        secondary.direction = input->direction.words;
        secondary.mode = optionalMode;
        FUN_00daf8e0(second, first, &modified, &primary, &secondary);
    } else {
        FUN_00daf8e0(second, first, &modified, &primary, 0);
    }
}