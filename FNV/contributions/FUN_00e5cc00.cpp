#include <xmmintrin.h>
struct __declspec(align(16)) HMat4 { __m128 c0,c1,c2,c3; };
struct MatrixHolder { int type; int flags; HMat4* matrix; };
struct AttrLookup {
    MatrixHolder* FUN_00e5c690(const char* name);
    int FUN_00e5cc00(const char* name, bool verbose, HMat4* result);
};
struct MessageBuilder {
    int storage;
    int length;
    int capacity;
    void FUN_00cb1600(char* buffer, unsigned int size);
    MessageBuilder* FUN_00cc01c0(const char*);
    MessageBuilder* FUN_00cc05a0(AttrLookup*);
    void FUN_00cc00e0();
};
struct AssertHandler {
    virtual void unused0();
    virtual void unused1();
    virtual void unused2();
    virtual void assertFailure(int enabled, unsigned int code, void* msg, const char* source, unsigned int line);
};
extern "C" AssertHandler* DAT_01268360;
extern "C" char DAT_010ecd74[];
extern "C" char DAT_010eccfc[];
extern "C" char DAT_010ecd0c[];
extern "C" char DAT_010eccc8[];
int AttrLookup::FUN_00e5cc00(const char* name, bool verbose, HMat4* result) {
    MatrixHolder* attribute = FUN_00e5c690(name);
    if (attribute) {
        __m128* source = reinterpret_cast<__m128*>(attribute->matrix);
        __m128* output = reinterpret_cast<__m128*>(result);
        output[0] = source[0];
        output[1] = source[1];
        output[2] = source[2];
        output[3] = source[3];
        return 0;
    }
    if (verbose) {
        __declspec(align(16)) void* scratch[0x80];
        MessageBuilder message;
        message.FUN_00cb1600(reinterpret_cast<char*>(scratch), 0x200);
        message.FUN_00cc01c0(DAT_010ecd74)
               ->FUN_00cc01c0(name)
               ->FUN_00cc01c0(DAT_010eccfc)
               ->FUN_00cc05a0(this)
               ->FUN_00cc01c0(DAT_010ecd0c);
        DAT_01268360->assertFailure(1, 0xabbaab81, scratch, DAT_010eccc8, 0xc4);
        message.FUN_00cc00e0();
    }
    return 1;
}