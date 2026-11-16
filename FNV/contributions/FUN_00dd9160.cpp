#include "h_74712c1d3c73.h"

// Stand-in for the polymorphic object stored in the game global at 0x01268364.
struct FUN_00dd9160_Global {
    virtual void vfn0();
    virtual void vfn1();
    virtual void vfn2();
    virtual unsigned int vfn3(unsigned int arg);   // vtable slot +0x0c
};

extern "C" FUN_00dd9160_Global* DAT_01268364;      // game global (0x01268364)
extern "C" int UNK_010d7c80;                       // game constant (0x010d7c80)

struct FUN_00dd9160_Class {
    void* unk00;            // +0x00: vtable pointer stand-in
    unsigned short unk04;   // +0x04
    unsigned short unk06;   // +0x06: state, set to 1
    unsigned int unk08;     // +0x08: result of the virtual call
    unsigned char unk0c;    // +0x0c: flag copied from the second parameter
    FUN_00dd9160_Class* FUN_00dd9160(unsigned int arg, unsigned char flag);
};

FUN_00dd9160_Class* FUN_00dd9160_Class::FUN_00dd9160(unsigned int arg, unsigned char flag) {
    unk06 = 1;
    unk00 = &UNK_010d7c80;
    unk0c = flag;
    unk08 = DAT_01268364->vfn3(arg);
    return this;
}
