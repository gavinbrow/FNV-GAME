struct Actor;
struct MagicCaster { Actor* FUN_00815410(); };
struct SourceA { Actor* FUN_00822b40(); };
struct FUN_0045cd60_shell { MagicCaster* FUN_0045cd60(); };
struct FUN_0080b660_class : FUN_0045cd60_shell {
    SourceA* FUN_0059bb30();
    void FUN_0080b660();
};
void __cdecl FUN_0080b850(Actor*, Actor*);
void FUN_0080b660_class::FUN_0080b660() {
    Actor* first = FUN_0059bb30() ? FUN_0059bb30()->FUN_00822b40() : (Actor*)0;
    Actor* second = FUN_0045cd60() ? FUN_0045cd60()->FUN_00815410() : (Actor*)0;
    if (first && second)
        FUN_0080b850(first, second);
}
