extern "C" double __cdecl sqrt(double value);

extern const float DAT_01095694;
extern const float DAT_01095698;
extern float DAT_011f3520;

// @fnv 0x00fb3ed0
void FUN_00fb3ed0()
{
    float inputValue = DAT_01095694;
    float roundedRoot;
    float squareRoot = static_cast<float>(sqrt(inputValue));
    roundedRoot = squareRoot;
    DAT_011f3520 = DAT_01095698 / roundedRoot;
}
