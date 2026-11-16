struct WorkerTarget {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    int unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    int unk40, unk44, unk48, unk4c, unk50, unk54;
    float targetValue;
};
struct WorkerAirFriction : NiPSysAirFieldAirFrictionCtlr {
    int unk0c, unk10, unk14, unk18, unk1c, unk20, unk24, unk28;
    int unk2c, unk30, unk34, unk38;
    WorkerTarget* target;
    void __thiscall FUN_00c307e0(volatile float value);
};
void WorkerAirFriction::FUN_00c307e0(float value) {
    WorkerTarget* p = target;
    float clamped = value;
    if (0.0 > clamped) clamped = 0.0f;
    if (1.0 < clamped) clamped = 1.0f;
    p->targetValue = clamped;
}
