struct FNVTimeClock {
    float GetTime();
};
extern FNVTimeClock g_GameClock;

struct FUN_0092cfd0_shell : MiddleLowProcess {
    bool FUN_0090a1a0(int packageType, bool forced);
    bool FUN_0092cfd0(int packageType, bool forced);
};

bool FUN_0092cfd0_shell::FUN_0092cfd0(int packageType, bool forced) {
    bool result;
    {
        float currentTime = g_GameClock.GetTime();
        result = false;
        if (forced || !GetCurrentPackage() || iHourPackageEvaluated != static_cast<int>(currentTime)) {
            result = FUN_0090a1a0(packageType, forced);
            iHourPackageEvaluated = static_cast<int>(currentTime);
        }
    }
    return result;
}