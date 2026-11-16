struct FUN_006757e0_shell : TESPackage {
    int FUN_00672f20();
    int FUN_0055b980();
    int FUN_00675c20(MobileObject* actor);
    int FUN_006751a0(MobileObject* actor);
    int FUN_006757e0(MobileObject* actor);
};

int FUN_006757e0_shell::FUN_006757e0(MobileObject* actor)
{
    int firstResult = FUN_00672f20();
    return firstResult == FUN_0055b980()
        ? FUN_00675c20(actor)
        : FUN_006751a0(actor);
}
