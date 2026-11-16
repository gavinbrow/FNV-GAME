struct Effect {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    int unk7c;
    int unk80;
    int unk84;
    int unk88;
    int unk8c;
    int unk90;
    int field94;
};
struct Source { Effect* FUN_00822b40(); };
struct Host { Source* FUN_0059bb30(); void FUN_0080e830(); };
void __cdecl FUN_0080ee50(int* value);
void Host::FUN_0080e830() {
    Effect* effect = FUN_0059bb30() ? FUN_0059bb30()->FUN_00822b40() : 0;
    if (effect)
        FUN_0080ee50(effect ? &effect->field94 : 0);
}
