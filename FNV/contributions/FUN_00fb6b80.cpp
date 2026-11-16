extern "C" double __cdecl sqrt(double value);

extern const float DAT_010a2d90;
extern const float DAT_010a2d94;
extern const double DAT_01011598;
extern float DAT_011f6c6c;

// @fnv 0x00fb6b80
void FUN_00fb6b80()
{
    float inputValue = DAT_010a2d90;
    float roundedRoot;
    float squareRoot = static_cast<float>(sqrt(inputValue));
    roundedRoot = squareRoot;
    DAT_011f6c6c = DAT_01011598 / (DAT_010a2d90 * roundedRoot) * DAT_010a2d94;
}
