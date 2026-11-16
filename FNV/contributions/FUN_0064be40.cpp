
struct FUN_0040fbf0_lock {
    void FUN_0040fbf0(int);
    void FUN_0040fba0();
};
struct FUN_0064be40_shell {
    bool FUN_0064be40(float elapsed, int unused);
    int FUN_0064bda0();
    void FUN_0064bf90(int deltaY, float* deltaX, float* limit, float elapsed);
    void FUN_0064c410(float x, float y);
};
struct FUN_00403e20_setting { float* FUN_00403e20(); };
extern FUN_00403e20_setting DAT_011d5924;
void __cdecl FUN_005330e0(float* value, float minimum, float maximum);

bool FUN_0064be40_shell::FUN_0064be40(float elapsed, int unused) {
    ((FUN_0040fbf0_lock*)((char*)this + 0x1a0))->FUN_0040fbf0(0);
    bool updateNeeded = !*(bool*)((char*)this + 0x18e);
    if (updateNeeded) {
        updateNeeded = true;
        int deltaY = FUN_0064bda0();
        float deltaX = *(float*)((char*)this + 0x150);
        float limit = *(float*)((char*)this + 0x154);
        if (deltaY < 15)
            FUN_0064bf90(deltaY, &deltaX, &limit, elapsed);
        float desiredX = deltaX - *(float*)((char*)this + 0x140);
        float stage = limit - *(float*)((char*)this + 0x144);
        float desiredY = *DAT_011d5924.FUN_00403e20() * elapsed;
        FUN_005330e0(&desiredX, -desiredY, desiredY);
        FUN_005330e0(&stage, -desiredY, desiredY);
        *(float*)((char*)this + 0x140) += desiredX;
        *(float*)((char*)this + 0x144) += stage;
        FUN_0064c410(*(float*)((char*)this + 0x140), *(float*)((char*)this + 0x144));
    }
    ((FUN_0040fbf0_lock*)((char*)this + 0x1a0))->FUN_0040fba0();
    return updateNeeded;
}