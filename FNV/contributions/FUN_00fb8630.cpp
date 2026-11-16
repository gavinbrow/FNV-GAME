// @fnv 0x00fb8630
extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" void __fastcall FUN_00afd230(int*);
struct FUN_00afc720_shell{void EnterInnerCriticalSection();};
struct Inner{void* v;volatile long count;};
struct RefArchive{char pad[0x158];Inner inner;};
struct NiArchivePointer{
 RefArchive* ptr;
 __forceinline NiArchivePointer():ptr(0){
  if(ptr){Inner* r=&ptr->inner;InterlockedIncrement(&r->count);}
 }
 __forceinline ~NiArchivePointer(){if(ptr)InterlockedDecrement(&ptr->inner.count);}
};
struct ArchivePtr {
 int value;
 __forceinline ArchivePtr(){FUN_00afd230(&value);}
 __forceinline ~ArchivePtr(){reinterpret_cast<FUN_00afc720_shell*>(this)->EnterInnerCriticalSection();}
};
struct ArchiveGlobal{
 NiArchivePointer root;ArchivePtr first[8],second[9];
 __forceinline ArchiveGlobal(){}
 __forceinline ~ArchiveGlobal(){}
};
ArchiveGlobal g_011f8190;