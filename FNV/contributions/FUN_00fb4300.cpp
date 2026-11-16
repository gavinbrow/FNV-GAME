extern "C" double __cdecl sqrt(double value);
extern const float DAT_010957ac;
extern const float DAT_010957b0;
extern float DAT_011f3598;

struct Calculation
{
    float result;
    float root;
    float argument;
};

// @fnv 0x00fb4300
extern "C" void FUN_00fb4300()
{
    Calculation calculation;
    calculation.argument = DAT_010957ac;
    calculation.result = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.result;
    DAT_011f3598 = DAT_010957b0 / calculation.root;
}
