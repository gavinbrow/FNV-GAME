extern "C" double __cdecl sqrt(double value);

extern const float DAT_01094ef0;
extern const float DAT_01094ef4;
extern float DAT_011f33b4;

// @fnv 0x00fb34d0
void FUN_00fb34d0()
{
    float inputValue = DAT_01094ef0;
    float roundedRoot;
    float squareRoot = static_cast<float>(sqrt(inputValue));
    roundedRoot = squareRoot;
    DAT_011f33b4 = DAT_01094ef4 / roundedRoot;
}
