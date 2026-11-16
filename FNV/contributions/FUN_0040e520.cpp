struct Actor;
struct MagicEffectKind {
    virtual void slot0();
    virtual void slot1();
    virtual void slot2();
    virtual void slot3();
    virtual void slot4();
    virtual void slot5();
    virtual int GetType();
};
struct SpellData {
    bool FUN_0040e210(int flag);
    int FUN_009e32d0();
};
struct ActorValues {
    int FUN_0066ef20(int id);
};
float __cdecl FUN_00649180(float cost, int value, int adjustment);
struct FUN_0040e520_shell {
    int FUN_004065e0();
    float FUN_004063e0(Actor* caster);
    float FUN_0040e520(Actor* caster);
};
float FUN_0040e520_shell::FUN_0040e520(Actor* caster) {
    float cost = 0.0f;
    Actor* effectiveCaster = (((MagicEffectKind*)((char*)this - 12))->GetType() == 2 ||
                              ((MagicEffectKind*)((char*)this - 12))->GetType() == 3) ? 0 : caster;
    if (((SpellData*)((char*)this - 36))->FUN_0040e210(1)) {
        cost = (float)((SpellData*)((char*)this - 36))->FUN_009e32d0();
        if (effectiveCaster) {
            cost = FUN_00649180(cost,
                ((ActorValues*)((char*)effectiveCaster + 0xa4))->FUN_0066ef20(FUN_004065e0()),
                ((ActorValues*)((char*)effectiveCaster + 0xa4))->FUN_0066ef20(11));
        }
    } else {
        cost = FUN_004063e0(effectiveCaster);
    }
    return cost;
}