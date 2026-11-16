extern "C" double __cdecl sqrt(double value);
extern const float DAT_010956c0;
extern const float DAT_010956c4;
extern float DAT_011f3530;

struct Calculation
{
    float result;
    float root;
    float argument;
};

// @fnv 0x00fb3fa0
extern "C" void FUN_00fb3fa0()
{
    Calculation calculation;
    calculation.argument = DAT_010956c0;
    calculation.result = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.result;
    DAT_011f3530 = DAT_010956c4 / calculation.root;
}
