struct NiColorA { float r, g, b, a; };
struct NiBSplineData {
    void FUN_00a526b0(float ratio, NiColorA* values, unsigned int components, void* controls, unsigned int index, float offset, float scale);
};
struct CompColorInterpolator {
    void* unk00;
    unsigned int unk04;
    float lastTime;
    float startTime;
    float endTime;
    NiBSplineData* spline;
    void* controlData;
    NiColorA cached;
    unsigned int startIndex;
    unsigned int unk30;
    float bias;
    float multiplier;
    char FUN_00a517a0(float time, void* unused, NiColorA* output);
};
char CompColorInterpolator::FUN_00a517a0(float time, void*, NiColorA* output) {
    if (lastTime == time) {
        *output = cached;
        return 1;
    }
    if (startIndex != 0xffff) {
        NiColorA values;
        NiColorA result;
        spline->FUN_00a526b0((time - startTime) / (endTime - startTime), &values, 4, controlData, startIndex, bias, multiplier);
        result.r = values.r;
        result.g = values.g;
        result.b = values.b;
        result.a = values.a;
        cached = result;
    }
    *output = cached;
    lastTime = time;
    return 1;
}