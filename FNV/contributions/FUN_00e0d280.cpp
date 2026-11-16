extern "C" void __cdecl FUN_00e0c700(void* object, int index, float amount);
extern "C" void __cdecl FUN_00e0d180(void* first, void* second, int index, int limit, float amount);
void __cdecl FUN_00e0d280(void* first, void* second, int index, int limit, float amount) {
    FUN_00e0c700(first, index, amount);
    FUN_00e0d180(first, second, index, limit, amount);
}
