extern "C" double __cdecl sqrt(double value);
extern const float DAT_01095730;
extern const float DAT_01095734;
extern float DAT_011f3558;

struct Calculation
{
    float result;
    float root;
    float argument;
};

// @fnv 0x00fb4140
extern "C" void FUN_00fb4140()
{
    Calculation calculation;
    calculation.argument = DAT_01095730;
    calculation.result = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.result;
    DAT_011f3558 = DAT_01095734 / calculation.root;
}
