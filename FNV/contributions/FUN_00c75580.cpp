
#include <xmmintrin.h>
extern "C" __declspec(align(16)) __m128 DAT_010c71b0;
struct RagController {
    unsigned char& controlFlag() { return *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this) + 0x43); }
    unsigned char& activeFlag() { return *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this) + 0xb1); }
    unsigned char& stateFlag() { return *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this) + 0xb3); }
    __m128& poseA() { return *reinterpret_cast<__m128*>(reinterpret_cast<char*>(this) + 0x120); }
    __m128& poseB() { return *reinterpret_cast<__m128*>(reinterpret_cast<char*>(this) + 0x170); }
    unsigned char& dirtyA() { return *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this) + 0x130); }
    unsigned char& dirtyB() { return *reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this) + 0x180); }
    void FUN_00c75580(unsigned char enabled);
};
void RagController::FUN_00c75580(unsigned char enabled) {
    int state;
    if (controlFlag() == 0) {
        if (activeFlag() != 0 && enabled != 0) {
            state = 1;
        } else {
            state = 0;
        }
    } else {
        state = stateFlag();
    }
    stateFlag() = (unsigned char)state;
    if (enabled == 0) {
        poseA() = DAT_010c71b0;
        poseB() = DAT_010c71b0;
        dirtyB() = 1;
        dirtyA() = 1;
    }
}