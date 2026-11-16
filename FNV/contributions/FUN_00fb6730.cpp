extern "C" double __cdecl sqrt(double value);
extern const float DAT_010a2c08;
extern const float DAT_010a2c0c;
extern float DAT_011f6c1c;

struct ScaleCalculation
{
    float squareRootResult;
    float root;
    float argument;
};

// @fnv 0x00fb6730
void FUN_00fb6730()
{
    ScaleCalculation calculation;
    calculation.argument = DAT_010a2c08;
    calculation.squareRootResult = static_cast<float>(sqrt(calculation.argument));
    calculation.root = calculation.squareRootResult;
    DAT_011f6c1c = DAT_010a2c0c / calculation.root;
}
