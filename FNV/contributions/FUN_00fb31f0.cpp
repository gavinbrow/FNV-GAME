extern "C" double __cdecl sqrt(double value);

extern const float DAT_01093f3c;
extern const float DAT_01093f40;
extern const double DAT_01011598;
extern float DAT_011f32ec;

// @fnv 0x00fb31f0
void FUN_00fb31f0()
{
    float inputValue = DAT_01093f3c;
    float roundedRoot;
    float squareRoot = static_cast<float>(sqrt(inputValue));
    roundedRoot = squareRoot;
    DAT_011f32ec = DAT_01011598 / (DAT_01093f3c * roundedRoot) * DAT_01093f40;
}
