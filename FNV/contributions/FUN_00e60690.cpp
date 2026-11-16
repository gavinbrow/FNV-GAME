struct InnerDispatch {
 virtual void f0(); virtual void f1(); virtual void f2(); virtual void f3(); virtual void f4(); virtual void run(int,int);
};
struct Dispatch { int x0,x4,x8,xc; InnerDispatch inner; };
struct FUN_00e60690_owner { int unk00; int unk04; int unk08; Dispatch* unk0c; int* unk10; void FUN_00e60690(int index,int value); };
void FUN_00e60690_owner::FUN_00e60690(int index,int value) { unk0c->inner.run(unk10[index],value); }
