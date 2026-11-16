void* __cdecl FUN_00aa1070(unsigned int);
extern "C" void* __cdecl FUN_00ec61c0(void*, int, unsigned int);
extern int DAT_010ade50;
struct B617FloatPart {
  int first, unused04; float x,y,z,w,scale,unused1c;
  B617FloatPart(){float zero=0.0f;x=zero;first=0;w=z=y=zero;scale=1.0f;}
};
struct B617IntPart {
 int index20,index24,index28;
 B617IntPart(){index28=0;index20=0;index24=0;}
};
struct B617Head {
 B617FloatPart f;
 B617IntPart i;
 ~B617Head();
};struct B617Holder {
    int index2c;
    int* vtable;
    int hashSize;
    void* hashTable;
    int count;
    B617Holder():index2c(0){}
    ~B617Holder();
};
struct FUN_00b617f0 : B617Head, B617Holder {
    FUN_00b617f0();
};
FUN_00b617f0::FUN_00b617f0() {
    vtable=&DAT_010ade18;
    hashSize=0x65;count=0;
    hashTable=FUN_00aa1070(0x194);
    FUN_00ec61c0(hashTable,0,hashSize*4);
    vtable=&DAT_010ade50;
}