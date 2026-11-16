extern "C" double __cdecl sqrt(double value);
extern const float DAT_010956c0;
extern const float DAT_010956c4;
extern float DAT_011f3534;
extern const double DAT_01011598;

struct Calculation
{
    float result;
    float root;
    float argument;
};

// @fnv 0x00fb3fe0
extern "C" void FUN_00fb3fe0()
{
    Calculation calculation;
    calculation.argument = DAT_010956c0;
    calculation.result = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.result;
    DAT_011f3534 = static_cast<float>(DAT_01011598 / (DAT_010956c0 * calculation.root) * DAT_010956c4);
}
