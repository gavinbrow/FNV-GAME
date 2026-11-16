struct NiObjectNET;
struct BaseStandIn { bool FUN_00c31530(NiObjectNET *); };
struct NiPSysModifier;
struct PsStandIn { NiPSysModifier *FUN_00c1b0f0(void *); };
struct NiObjectNET : PsStandIn {};
struct NiPSysModifier {
    virtual void v0();
    virtual void v1();
    virtual NiPSysModifier *GetNextModifier();
    NiPSysModifier *next;
};
struct GlobalObjectO2_00a7b610 { int unk00; int unk04; };
extern GlobalObjectO2_00a7b610 g_012027a8;
struct FUN_00c306f0_class : BaseStandIn {
    bool FUN_00c306f0(NiObjectNET *);
};
bool FUN_00c306f0_class::FUN_00c306f0(NiObjectNET *target) {
    if (!FUN_00c31530(target))
        return false;
    NiPSysModifier *modifier = target->FUN_00c1b0f0((char *)this + 0x38);
    if (!modifier)
        return false;
    NiPSysModifier *item = modifier->GetNextModifier();
    while (item) {
        if (item == (NiPSysModifier *)&g_012027a8)
            return true;
        item = item->next;
    }
    return false;
}

