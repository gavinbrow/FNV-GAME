extern "C" double __cdecl sqrt(double value);

extern const float DAT_01095474;
extern const float DAT_01095478;
extern float DAT_011f34d8;

// @fnv 0x00fb3d30
void FUN_00fb3d30()
{
    float inputValue = DAT_01095474;
    float roundedRoot;
    float squareRoot = static_cast<float>(sqrt(inputValue));
    roundedRoot = squareRoot;
    DAT_011f34d8 = DAT_01095478 / roundedRoot;
}
