// @fnv 0x00ec9760
struct Object { int reserved; };
extern Object DAT_011c26a0;
void __fastcall FUN_00ed60eb(int retained, Object* object);
void __fastcall FUN_00ec9760(int retained) { FUN_00ed60eb(retained, &DAT_011c26a0); }