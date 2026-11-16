extern "C" unsigned char DAT_010f1ee0;
extern "C" void __cdecl FUN_00ed16a2(void*);
struct TypeInfo { void* vftable; void FUN_00ec409b(); };
void TypeInfo::FUN_00ec409b() {
  vftable = &DAT_010f1ee0;
  FUN_00ed16a2(this);
}
