extern const double DAT_01012060;
struct WeightAccessor { float FUN_006042d0(); };
struct FUN_00604250_shell : TESNPC {
    int FUN_0084e3a0();
    WeightAccessor* FUN_004ac110();
    WeightAccessor* FUN_004ac110(void*);
    void* FUN_005f0cc0();
    float FUN_00944300();
    float FUN_00604250();
};
float FUN_00604250_shell::FUN_00604250()
{
    if (FUN_0084e3a0() == 7) {
        return fWeight == DAT_01012060 && FUN_004ac110()
            ? FUN_004ac110(FUN_005f0cc0())->FUN_006042d0()
            : fWeight;
    }
    return FUN_00944300();
}