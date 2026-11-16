struct FUN_00c2f3f0Target {
    char _pad[0x64];
    float unk64;
};

struct NiPSysSpawnModifier {
    char _pad[0x3c];
    FUN_00c2f3f0Target* unk3c;
    void __thiscall FUN_00c2f3f0(float fValue);
};

double g_01012060 = 0.0;
double g_01012070 = 1.0;

void __thiscall NiPSysSpawnModifier::FUN_00c2f3f0(float fValue) {
    FUN_00c2f3f0Target* target = this->unk3c;
    float value = fValue;

    if (value < g_01012060) {
        value = 0.0f;
    }
    if (value > g_01012070) {
        value = 1.0f;
    }

    target->unk64 = value;
}