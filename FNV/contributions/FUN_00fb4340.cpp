extern "C" double __cdecl sqrt(double value);
extern const float DAT_010957ac;
extern const float DAT_010957b0;
extern float DAT_011f359c;
extern const double DAT_01011598;

struct Calculation
{
    float result;
    float root;
    float argument;
};

// @fnv 0x00fb4340
extern "C" void FUN_00fb4340()
{
    Calculation calculation;
    calculation.argument = DAT_010957ac;
    calculation.result = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.result;
    DAT_011f359c = static_cast<float>(DAT_01011598 / (DAT_010957ac * calculation.root) * DAT_010957b0);
}
