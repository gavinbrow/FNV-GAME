extern "C" double __cdecl sqrt(double value);

extern const float DAT_010a2d4c;
extern const float DAT_010a2d50;
extern const double DAT_01011598;
extern float DAT_011f6c58;

// @fnv 0x00fb6ab0
void FUN_00fb6ab0()
{
    float inputValue = DAT_010a2d4c;
    float roundedRoot;
    float squareRoot = static_cast<float>(sqrt(inputValue));
    roundedRoot = squareRoot;
    DAT_011f6c58 = DAT_01011598 / (DAT_010a2d4c * roundedRoot) * DAT_010a2d50;
}
