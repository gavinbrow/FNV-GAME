// @fnv 0x00ec976a
struct Object { int reserved; };
extern Object DAT_011c26a0;
void __fastcall FUN_00ed6070(int retained, Object* object);
void __fastcall FUN_00ec976a(int retained) { FUN_00ed6070(retained, &DAT_011c26a0); }