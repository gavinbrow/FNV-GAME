extern "C" double __cdecl sqrt(double value);
extern const float DAT_010a2d4c;
extern const float DAT_010a2d50;
extern float DAT_011f6c5c;

struct ScaleCalculation
{
    float squareRootResult;
    float root;
    float argument;
};

// @fnv 0x00fb6a70
void FUN_00fb6a70()
{
    ScaleCalculation calculation;
    calculation.argument = DAT_010a2d4c;
    calculation.squareRootResult = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.squareRootResult;
    DAT_011f6c5c = DAT_010a2d50 / calculation.root;
}
