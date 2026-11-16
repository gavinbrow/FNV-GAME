// @fnv 0x00ec3260
extern "C" void __cdecl FUN_00ec3adf(void *pointer);
void __cdecl operator delete(void *pointer) throw();
extern "C" void __fastcall FUN_00ec3260(void **pointer)
{
    FUN_00ec3adf(*pointer);
    ::operator delete(*pointer);
}