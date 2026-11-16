struct CopiedState {
    void FUN_006e5cc0(CopiedState* other);
};
struct FUN_0080e7e0_Class : ActiveEffect {
    void* unk04; void* unk08; void* unk0c; void* unk10;
    void* unk14; void* unk18; void* unk1c; void* unk20;
    void* unk24; void* unk28; void* unk2c; void* unk30;
    void* unk34; void* unk38; void* unk3c; void* unk40;
    void* unk44;
    CopiedState state48;
    void FUN_00804090(ActiveEffect* other);
    void FUN_0080e7e0(ActiveEffect* other);
};
void FUN_0080e7e0_Class::FUN_0080e7e0(ActiveEffect* other)
{
    FUN_00804090(other);
    LightEffect* effect = dynamic_cast<LightEffect*>(other);
    if (effect) {
        reinterpret_cast<FUN_0080e7e0_Class*>(effect)->state48.FUN_006e5cc0(&state48);
    }
}