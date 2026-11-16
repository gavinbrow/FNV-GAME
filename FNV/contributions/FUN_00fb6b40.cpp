extern "C" double __cdecl sqrt(double value);
extern const float DAT_010a2d90;
extern const float DAT_010a2d94;
extern float DAT_011f6c70;

// @fnv 0x00fb6b40
void FUN_00fb6b40()
{
    float inputValue = DAT_010a2d90;
    float roundedRoot;
    float squareRoot = static_cast<float>(sqrt(inputValue));
    roundedRoot = squareRoot;
    DAT_011f6c70 = DAT_010a2d94 / roundedRoot;
}
