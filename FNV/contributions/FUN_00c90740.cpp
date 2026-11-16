struct FUN_00c90740_guard { int unk00, unk04, active, recursion, unk10, unk14, criticalSection; };
extern unsigned long DAT_012681d8;
extern "C" __declspec(dllimport) void* __stdcall TlsGetValue(unsigned long);
extern "C" __declspec(dllimport) int __stdcall TlsSetValue(unsigned long, const void*);
extern "C" __declspec(dllimport) void __stdcall EnterCriticalSection(void*);
extern "C" __declspec(dllimport) void __stdcall LeaveCriticalSection(void*);
void __cdecl FUN_00c90740(void* items, int count, int stride) {
 FUN_00c90740_guard* guard=(FUN_00c90740_guard*)DAT_012681d4;
 if (guard->active != 0 && TlsGetValue(DAT_012681d8) != (void*)0x23df4554) {
  if (TlsGetValue(DAT_012681d8) == (void*)0x23df4554) ++guard->recursion;
  else { EnterCriticalSection(&guard->criticalSection); guard->recursion=1; TlsSetValue(DAT_012681d8, (void*)0x23df4554); }
  if (count>0) { char* item=(char*)items; do { (*((FUN_00c903b0_class**)item))->FUN_00c903b0(); item+=stride; }while(--count); }
  if (--guard->recursion<=0) { TlsSetValue(DAT_012681d8, 0); LeaveCriticalSection(&guard->criticalSection); }
 } else {
  if (count>0) {
int remaining=count; int step=*(volatile int*)&stride; char* item=(char*)items; do { (*((FUN_00c903b0_class**)item))->FUN_00c903b0(); item+=step; }while(--remaining);
  }
 }
}