
__declspec(thread) int fnvThreadMemoryBase;
__forceinline int& threadMemoryMode() {
  return *reinterpret_cast<int*>(reinterpret_cast<char*>(&fnvThreadMemoryBase) + 0x2b4);
}
struct MemoryContextScope {
  int savedMode;
  __forceinline explicit MemoryContextScope(int n){savedMode=threadMemoryMode();threadMemoryMode()=n;}
  __forceinline ~MemoryContextScope(){threadMemoryMode()=savedMode;}
};
struct ResourceOne { void __thiscall FUN_00d055c0(); };
struct ResourceTwo { void __thiscall FUN_00c905b0(); };
struct ResourceDisposer { virtual void reserved0(); virtual void reserved1(); virtual void dispose(ResourceOne*,int); };
struct ResourceService { int unk00,unk04,unk08,unk0c; ResourceDisposer* disposer; };
extern "C" ResourceService* __cdecl FUN_00c85750();
struct FUN_00cbf2f0_class {
 int unk00,unk04,unk08; int active; int unk10;
 ResourceOne* first; ResourceTwo* second;
 void __thiscall FUN_00cbf2f0();
};
void FUN_00cbf2f0_class::FUN_00cbf2f0() {
 MemoryContextScope memoryContext(0x10);
 if(active!=0){
  ResourceOne* owned=first;
  if(owned!=0){
   owned->FUN_00d055c0();
   ResourceService* s=FUN_00c85750(); ResourceDisposer* p=s->disposer; p->dispose(owned,0x1c0);
  }
  first=0;
  if(second!=0)second->FUN_00c905b0();
  second=0;
 }
 active=0;
}
