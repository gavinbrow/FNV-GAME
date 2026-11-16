struct Allocator { virtual void v00(); virtual void* allocate(int); virtual void v08(); virtual void v0c(); __declspec(nothrow) virtual void freeBlock(void*,int); };
struct Router {int unk00,unk04,unk08,unk0c; Allocator* heap; Allocator& getHeap() {return *heap;} };
__declspec(nothrow) Router& __cdecl FUN_00c85750();
struct Vector4 {float x,y,z,w;};
struct VectorArray {Vector4* data; int size; int capacity;
 VectorArray():data(0),size(0),capacity(0x80000000) {}
 void release(Allocator& heap) {size=0; if(!(capacity&0x80000000)) heap.freeBlock(data,(capacity&0x3fffffff)*16);}
 
};
struct Options {unsigned int unk00,unk04; unsigned char flag08,flag09,flag0a,flag0b; unsigned int unk0c; __declspec(nothrow) void FUN_00d74d40();};
struct FUN_00d76ca0 {__declspec(nothrow) virtual ~FUN_00d76ca0(); unsigned short memorySize,referenceCount; int unk08,unk0c,unk10;
 __declspec(nothrow) FUN_00d76ca0();
 static void* allocate(Allocator& heap,unsigned int bytes) { void* memory=heap.allocate(bytes); ((FUN_00d76ca0*)memory)->memorySize=(unsigned short)bytes; return memory;}
 static void* operator new(unsigned int bytes) {return allocate(FUN_00c85750().getHeap(),bytes);}
 __declspec(nothrow) void FUN_00d771c0(Vector4*,int,const Options&);
 __declspec(nothrow) int FUN_00d74e10();
};
struct Hull {
unsigned int unk00;
unsigned int unk04;
unsigned int unk08;
unsigned int unk0c;
unsigned int unk10;
unsigned int unk14;
int count;
unsigned int unk1c;
unsigned int unk20;
unsigned int unk24;
unsigned int unk28;
unsigned int unk2c;
unsigned int unk30;
unsigned int unk34;
unsigned int unk38;
unsigned int unk3c;
unsigned int unk40;
unsigned int unk44;
unsigned int unk48;
unsigned int unk4c;
unsigned int unk50;
unsigned int unk54;
unsigned int unk58;
unsigned int unk5c;
unsigned int unk60;
unsigned int unk64;
unsigned int unk68;
unsigned int unk6c;
unsigned int unk70;
unsigned int unk74;
unsigned int unk78;
unsigned int unk7c;
unsigned int unk80;
unsigned int unk84;
unsigned int unk88;
unsigned int unk8c;
unsigned int unk90;
unsigned int unk94;
unsigned int unk98;
unsigned int unk9c;
unsigned int unka0;
unsigned int unka4;
unsigned int unka8;
unsigned int unkac;
unsigned int unkb0;
unsigned int unkb4;
unsigned int unkb8;
unsigned int unkbc;
unsigned int unkc0;
unsigned int unkc4;
unsigned int unkc8;
unsigned int unkcc;
unsigned int unkd0;
unsigned int unkd4;
unsigned int unkd8;
unsigned int unkdc;
unsigned int unke0;
FUN_00d76ca0* builder;
 __declspec(nothrow) void FUN_00e114c0();
 __declspec(nothrow) void FUN_00e12640(VectorArray&);
 bool FUN_00e13750();
};
bool Hull::FUN_00e13750() {
 FUN_00e114c0();
 if(count>3) {
  Options options; options.FUN_00d74d40(); options.flag09=0; options.flag0a=1;
  builder=new FUN_00d76ca0;
  VectorArray vertices;
  FUN_00e12640(vertices);
  builder->FUN_00d771c0(vertices.data,vertices.size,options);
  if(builder->FUN_00d74e10()!=3) {
   delete builder;
   builder=0;
   vertices.release(FUN_00c85750().getHeap());
   return false;
  }
  vertices.release(FUN_00c85750().getHeap());
 }
 return true;
}




