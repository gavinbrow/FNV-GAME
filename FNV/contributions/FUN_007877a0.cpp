extern int DAT_01071b64;
void* __cdecl FUN_00a00940(const void* data, int flags);
struct LevelOption { bool __thiscall FUN_00a01230(void* data); };
struct FUN_007877a0_Object { bool FUN_007877a0(LevelOption* option); };
bool FUN_007877a0_Object::FUN_007877a0(LevelOption* option) {
    static void* cached = FUN_00a00940(&DAT_01071b64, -1);
    return cached != 0 && option != 0 && option->FUN_00a01230(cached);
}