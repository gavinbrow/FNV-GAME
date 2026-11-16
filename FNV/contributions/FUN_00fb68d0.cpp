extern "C" double __cdecl sqrt(double value);
extern const float DAT_010a2d1c;
extern const float DAT_010a2d20;
extern float DAT_011f6c3c;

struct ScaleCalculation
{
    float squareRootResult;
    float root;
    float argument;
};

// @fnv 0x00fb68d0
void FUN_00fb68d0()
{
    ScaleCalculation calculation;
    calculation.argument = DAT_010a2d1c;
    calculation.squareRootResult = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.squareRootResult;
    DAT_011f6c3c = DAT_010a2d20 / calculation.root;
}
