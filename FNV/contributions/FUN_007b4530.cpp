
extern "C" const double DAT_01012060;
struct ActiveEffectEntry {
    float FUN_00a011b0(unsigned int id);
    void FUN_00a012d0(unsigned int id, float value, bool update);
};
struct ActiveEffectCollection {
    unsigned int unk00,unk04,unk08,unk0c,unk10,unk14;
    float rate;
    int FUN_00559450();
    ActiveEffectEntry*** FUN_0057cbe0(int* iterator);
    void FUN_007b4530(int amount);
};
void ActiveEffectCollection::FUN_007b4530(int amount) {
    if (rate <= DAT_01012060)
        return;
    int it = FUN_00559450();
    while (it) {
        ActiveEffectEntry* pEffect = **FUN_0057cbe0(&it);
        float fAmount = pEffect->FUN_00a011b0(4002);
        fAmount = (float)amount * rate + fAmount;
        pEffect->FUN_00a012d0(4002,fAmount,true);
    }
}
