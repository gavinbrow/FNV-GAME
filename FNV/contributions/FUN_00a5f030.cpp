extern void* __cdecl FUN_00aa13e0(unsigned int);
extern int DAT_0109b5ac;
extern int DAT_0101fbd4;
struct NiObjectBase { void __thiscall FUN_00a5aa20(); };
struct ObjectState { void* reference; unsigned int count; unsigned short first; unsigned short second; unsigned short third; unsigned short enabled; };
NiObjectBase* __cdecl FUN_00a5f030() {
 NiObjectBase* object = static_cast<NiObjectBase*>(FUN_00aa13e0(0xac));
 if(object) {
  object->FUN_00a5aa20();
  *reinterpret_cast<void**>(object) = &DAT_0109b5ac;
  ObjectState* state = reinterpret_cast<ObjectState*>(reinterpret_cast<char*>(object)+0x9c);
  state->first = 0;
  state->enabled = 1;
  state->second = 0;
  state->third = 0;
  state->count = 0;
  state->reference = &DAT_0101fbd4;
  return object;
 }
 return 0;
}