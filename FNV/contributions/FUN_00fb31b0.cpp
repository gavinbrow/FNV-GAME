extern "C" double __cdecl sqrt(double value);

extern const float DAT_01093f3c;
extern const float DAT_01093f40;
extern float DAT_011f32e8;

// @fnv 0x00fb31b0
void FUN_00fb31b0()
{
    float inputValue = DAT_01093f3c;
    float roundedRoot;
    float squareRoot = static_cast<float>(sqrt(inputValue));
    roundedRoot = squareRoot;
    DAT_011f32e8 = DAT_01093f40 / roundedRoot;
}
