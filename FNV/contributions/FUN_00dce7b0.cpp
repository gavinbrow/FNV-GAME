struct LocalContext { void* vtable; };
extern int DAT_010d77c0;
extern "C" void __cdecl FUN_00dcea10(int, int, int, LocalContext*);
void __cdecl FUN_00dce7b0(int first, int second, int third) {
    LocalContext local;
    local.vtable = &DAT_010d77c0;
    FUN_00dcea10(first, second, third, &local);
}
