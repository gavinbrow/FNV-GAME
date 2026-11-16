extern int DAT_010cb830;
extern int DAT_0102e388;
struct FnvRefObject {void FUN_00c905b0() throw();};
struct FnvMemoryManager {
 virtual void f0();virtual void f1();virtual void f2();virtual void f3();
 virtual void release(void*,unsigned int) throw();
};
struct FnvRouter {void* a;void* b;void* c;void* d; FnvMemoryManager* manager;};
FnvRouter* FUN_00c85750();
struct FnvArray {
 void** data; int size; unsigned int capacityAndFlags;
 ~FnvArray() throw(){
   FnvRouter* router = FUN_00c85750();FnvMemoryManager* mgr=router->manager;
   unsigned int cap = capacityAndFlags;
   size=0;
   if(!(cap & 0x80000000u))
      mgr->release(data,(cap & 0x3fffffffu)*4);
   data=0; capacityAndFlags=0x80000000u;
 }
};
struct FnvParent {
 void* vtbl;
 unsigned short flags; short references;
 ~FnvParent() throw(){vtbl=&DAT_0102e388;}
};
struct FUN_00ce2600:FnvParent {
 FnvArray bodies, constraints, mapping; FnvRefObject* skeleton;
 ~FUN_00ce2600() throw();
};
FUN_00ce2600::~FUN_00ce2600() throw(){
 vtbl=&DAT_010cb830;
 for(int i=0;i<bodies.size;++i) ((FnvRefObject*)bodies.data[i])->FUN_00c905b0();
 for(int j=0;j<constraints.size;++j) ((FnvRefObject*)constraints.data[j])->FUN_00c905b0();
 if(skeleton) skeleton->FUN_00c905b0(); skeleton=0;
}