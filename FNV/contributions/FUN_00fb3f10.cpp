extern "C" double __cdecl sqrt(double value);

extern const float DAT_01095694;
extern const float DAT_01095698;
extern const double DAT_01011598;
extern float DAT_011f3524;

// @fnv 0x00fb3f10
void FUN_00fb3f10()
{
    float inputValue = DAT_01095694;
    float roundedRoot;
    float squareRoot = static_cast<float>(sqrt(inputValue));
    roundedRoot = squareRoot;
    DAT_011f3524 = DAT_01011598 / (DAT_01095694 * roundedRoot) * DAT_01095698;
}
