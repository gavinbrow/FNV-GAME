extern "C" double __cdecl sqrt(double value);
extern const float DAT_010a2d34;
extern const float DAT_010a2d38;
extern float DAT_011f6c4c;

struct ScaleCalculation
{
    float squareRootResult;
    float root;
    float argument;
};

// @fnv 0x00fb69a0
void FUN_00fb69a0()
{
    ScaleCalculation calculation;
    calculation.argument = DAT_010a2d34;
    calculation.squareRootResult = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.squareRootResult;
    DAT_011f6c4c = DAT_010a2d38 / calculation.root;
}
