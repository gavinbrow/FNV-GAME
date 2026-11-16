extern "C" char* __cdecl FUN_00ed11de();
// @fnv 0x00ece56e
extern "C" bool __cdecl FUN_00ece56e()
{
    char* object = FUN_00ed11de();
    return *reinterpret_cast<int*>(object + 0x90) != 0;
}
