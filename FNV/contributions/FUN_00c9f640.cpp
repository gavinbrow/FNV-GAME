void __cdecl FUN_00c876f0();
void __cdecl FUN_00c87700();
struct ProjectileCreator {
    void __thiscall FUN_00c85900(Object_00c9f5a0* projectile, int mode);
    Object_00c9f5a0* __thiscall FUN_00c9f640(int mode);
};
Object_00c9f5a0* ProjectileCreator::FUN_00c9f640(int mode) {
    FUN_00c876f0();
    Object_00c9f5a0* projectile = new Object_00c9f5a0;
    FUN_00c85900(projectile, mode);
    FUN_00c87700();
    return projectile;
}