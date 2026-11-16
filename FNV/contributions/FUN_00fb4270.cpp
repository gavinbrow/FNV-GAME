extern "C" double __cdecl sqrt(double value);
extern const float DAT_01095744;
extern const float DAT_01095748;
extern float DAT_011f358c;
extern const double DAT_01011598;

struct Calculation
{
    float result;
    float root;
    float argument;
};

// @fnv 0x00fb4270
extern "C" void FUN_00fb4270()
{
    Calculation calculation;
    calculation.argument = DAT_01095744;
    calculation.result = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.result;
    DAT_011f358c = static_cast<float>(DAT_01011598 / (DAT_01095744 * calculation.root) * DAT_01095748);
}
