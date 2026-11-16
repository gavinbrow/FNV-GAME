struct Actor;
struct ListNode
{
    void* value;
    ListNode* _ref_00726070();
    bool _ref_008256d0() const;
    struct ActiveEffect** _ref_006815c0();
};
struct PlayerEffects
{
    virtual void slot0();
    virtual void slot1();
    virtual ListNode* GetFirst();
};
struct Actor
{
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c; int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68; int unk6c; int unk70; int unk74; int unk78; int unk7c;
    int unk80; int unk84; int unk88; int unk8c; int unk90;
    PlayerEffects effects;
};
extern Actor* g_thePlayer;
struct ActiveEffect;
struct EffectSetting
{
    bool IsAssociatedFormUsed();
    bool IsFlagSet(unsigned int flag);
};
struct ActiveEffect
{
    EffectSetting* GetEffectSetting();
    float GetAge();
    void Dispel(bool immediate);
};
struct GlobalObject2_0040c150 { int* FUN_0043d4d0(); };
extern GlobalObject2_0040c150 g_011d171c;
extern float DAT_01015f5c;

struct FUN_00829970_Class { void FUN_00829970(); };
void FUN_00829970_Class::FUN_00829970()
{
    ListNode* node = g_thePlayer->effects.GetFirst();
    int bestAge;
    ActiveEffect* bestEffect;
    float validCount;
    bestEffect = 0;
    validCount = DAT_01015f5c;
    bestAge = 0;
    while (node && !node->_ref_008256d0())
    {
            ActiveEffect* effect = *node->_ref_006815c0();
            EffectSetting* setting = effect->GetEffectSetting();
            if (setting->IsAssociatedFormUsed() && setting->IsFlagSet(0x40000))
            {
                ++bestAge;
                if (effect->GetAge() > validCount)
                {
                    bestEffect = effect;
                    validCount = effect->GetAge();
                }
            }
        node = node->_ref_00726070();
    }
    if (bestEffect && bestAge > *g_011d171c.FUN_0043d4d0())
        bestEffect->Dispel(false);
}








