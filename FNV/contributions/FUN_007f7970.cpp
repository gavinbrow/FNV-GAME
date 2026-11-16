struct FalloffPair {
    float first;
    float second;
    void __thiscall FUN_006815c0();
};

struct FalloffController {
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
    bool active;
    unsigned char state29;
    unsigned short state2a;
    float startTime;
    float firstDuration;
    float secondDuration;
    float firstStrength;
    float secondStrength;
    float firstRate;
    float secondRate;
    float firstOutput;
    float secondOutput;

    void __thiscall FUN_007f7970(float currentTime);
};

float __cdecl FUN_004e44d0(float value);
void __cdecl FUN_007f7a50(float first, float second);

void __thiscall FalloffController::FUN_007f7970(float currentTime)
{
    float elapsed = currentTime - startTime;
    if (elapsed > firstDuration && elapsed > secondDuration) {
        active = false;
        FUN_007f7a50(0.0f, 0.0f);
    } else {
        FalloffPair falloff;
        falloff.FUN_006815c0();
        falloff.first = 1.0f - elapsed / firstDuration;
        falloff.second = 1.0f - elapsed / secondDuration;
        firstOutput = FUN_004e44d0(elapsed * firstRate) * firstStrength * falloff.first;
        secondOutput = FUN_004e44d0(elapsed * secondRate) * secondStrength * falloff.second;
    }
}
