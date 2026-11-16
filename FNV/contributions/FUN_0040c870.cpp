struct MagicItemCompare {
    virtual void vfn_0();
    virtual void vfn_4();
    virtual void vfn_8();
    virtual void vfn_c();
    virtual void vfn_10();
    virtual void vfn_14();
    virtual void vfn_18();
    virtual void vfn_1c();
    virtual void vfn_20();
    virtual void vfn_24();
    virtual void vfn_28();
    virtual void vfn_2c();
    virtual bool CompareMagic(MagicItem* other);
    char name[8];
};
struct EffectListCompare { bool FUN_00405a00(EffectItemList* other); };
struct MagicItemObjectShell : TESForm, MagicItemCompare {
    EffectItemList effectList;
    bool FUN_00485270(TESForm* other);
    bool FUN_0040c870(TESForm* other);
};
bool MagicItemObjectShell::FUN_0040c870(TESForm* other)
{
    MagicItemObject* converted = dynamic_cast<MagicItemObject*>(other);
    if (!converted) return true;
    if (FUN_00485270(other)) return true;
    if (CompareMagic(static_cast<MagicItem*>(converted))) return true;
    if (reinterpret_cast<EffectListCompare*>(&effectList)
          ->FUN_00405a00(converted ? &converted->effectList : 0)) return true;
    return false;
}
