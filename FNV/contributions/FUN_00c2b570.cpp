struct PlanarAngleControllerData {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    float unk28;
};
struct FUN_00c2b570_class : NiPSysEmitterPlanarAngleCtlr {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    int unk28;
    int unk2C;
    int unk30;
    int unk34;
    int unk38;
    PlanarAngleControllerData* unk3C;
    void __thiscall FUN_00c2b570(float fValue);
};
void __thiscall FUN_00c2b570_class::FUN_00c2b570(float fValue) {
    unk3C->unk28 = fValue;
}
