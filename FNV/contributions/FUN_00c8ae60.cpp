extern void* __cdecl FUN_00aa13e0(unsigned int size);
extern int DAT_01030bf4;
extern int DAT_010c44e4;
extern int DAT_010c485c;
extern int DAT_012680f8;
extern int DAT_012686d0;
extern int DAT_012681a0;

struct Base_00c8ae60 {
    int* vtable;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    void FUN_00c87c30();
    Base_00c8ae60() { FUN_00c87c30(); }
};
struct Object_00c8ae60 : Base_00c8ae60 {
    static void* operator new(unsigned int bytes) { return FUN_00aa13e0(bytes); }
    Object_00c8ae60() {
        vtable = &DAT_01030bf4;
        unk0c = 0;
        unk10 = 0;
        ++DAT_012680f8;
        vtable = &DAT_010c44e4;
        ++DAT_012686d0;
        vtable = &DAT_010c485c;
        ++DAT_012681a0;
    }
};
Object_00c8ae60* __cdecl FUN_00c8ae60()
{
    return new Object_00c8ae60;
}