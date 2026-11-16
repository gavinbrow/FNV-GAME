struct S_00ba63e0_MM { void* __thiscall Allocate(unsigned int); void __thiscall Deallocate(void*); };
extern S_00ba63e0_MM DAT_011f6238;
class NiObject { public: NiObject(); virtual void v0(); virtual ~NiObject(); int unk04; };
struct S_00ba63e0_Elem { char unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; S_00ba63e0_Elem(); static void* operator new[](unsigned int n) { return DAT_011f6238.Allocate(n); } static void operator delete[](void* p) { DAT_011f6238.Deallocate(p); } };
struct S_00ba63e0_ArrBase { virtual ~S_00ba63e0_ArrBase(); void** unk04; unsigned short unk08; unsigned short unk0a; unsigned short unk0c; unsigned short unk0e; S_00ba63e0_ArrBase() { unk08=0; unk0e=1; unk0a=0; unk0c=0; unk04=0; } };
struct S_00ba63e0_Arr : S_00ba63e0_ArrBase { virtual ~S_00ba63e0_Arr(); void RemoveAll() { for(unsigned short i=0;i<unk0a;i++) unk04[i]=0; unk0a=0; unk0c=0; } };
struct FUN_00ba63e0 : NiObject { int unk08; unsigned short unk0c; int unk10; S_00ba63e0_Elem* unk14; int unk18; S_00ba63e0_Arr unk1c; FUN_00ba63e0(unsigned short a,unsigned int n); virtual ~FUN_00ba63e0(); };
FUN_00ba63e0::FUN_00ba63e0(unsigned short a,unsigned int n) { unk08=0; unk0c=a; unk10=n; unk14=new S_00ba63e0_Elem[n]; unk1c.RemoveAll(); unk18=0; }