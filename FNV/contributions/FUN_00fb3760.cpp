extern "C" double __cdecl sqrt(double value);

extern const float DAT_010950a0;
extern const float DAT_010950a4;
extern float DAT_011f340c;

// @fnv 0x00fb3760
void FUN_00fb3760()
{
    float inputValue = DAT_010950a0;
    float roundedRoot;
    float squareRoot = static_cast<float>(sqrt(inputValue));
    roundedRoot = squareRoot;
    DAT_011f340c = DAT_010950a4 / roundedRoot;
}
