// @fnv 0x00ec3b9a
extern "C" void __cdecl FUN_00ec3b5a();
extern "C" int __cdecl atexit(void (__cdecl* destructor)());
extern "C" unsigned char __cdecl FUN_00ec3b9a() { return atexit(&FUN_00ec3b5a) != 0 ? 24 : 0; }
