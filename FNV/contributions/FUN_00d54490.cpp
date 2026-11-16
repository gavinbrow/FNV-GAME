#include <xmmintrin.h>
#include "h_49490046a897.h"
extern char DAT_010d0d70;
struct S00d54490_Ref { void FUN_00c90510(); };
struct S00d54490_Obj {
    void* volatile unk00;
    unsigned char unk04;
    unsigned char unk05;
    unsigned short volatile unk06;
    int volatile unk08;
    int unk0C;
    volatile unsigned char unk10;
    void* unk14;
    int unk18;
    int unk1C;
    float unk20[4];
    S00d54490_Obj* __thiscall FUN_00d54490(int arg1,const hkpMoppBvTreeShape& arg2);
};
S00d54490_Obj* __thiscall S00d54490_Obj::FUN_00d54490(int arg1,const hkpMoppBvTreeShape& arg2)
{
    const hkpMoppBvTreeShape* src=&arg2;
    this->unk06=1;
    this->unk08=0;
    this->unk0C=arg1;
    this->unk10=0;
    this->unk00=&DAT_010d0d70;
    this->unk14=const_cast<hkpMoppBvTreeShape*>(src);
    reinterpret_cast<S00d54490_Ref*>(const_cast<hkpMoppBvTreeShape*>(src))->FUN_00c90510();
    *reinterpret_cast<__m128*>(&this->unk20)=*reinterpret_cast<const __m128*>(reinterpret_cast<const char*>(src)+0x10);
    this->unk18=*reinterpret_cast<const int*>(reinterpret_cast<const char*>(src)+0x20);
    this->unk1C=*reinterpret_cast<const int*>(reinterpret_cast<const char*>(src)+0x24);
    return this;
}