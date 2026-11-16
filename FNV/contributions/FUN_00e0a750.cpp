extern "C" double DAT_01011588;
extern "C" double DAT_01021928;
extern "C" double DAT_010ea600;
extern "C" double DAT_010737c8;
extern "C" float DAT_010ea608;
struct FNVRange { int begin,end; float lower,upper,defaultFactor; int unk14,unk18,unk1c; float value; };
struct FNVResponse { int unk00,unk04,unk08,unk0c,unk10; float magnitude; int unk18; float maximum; float FUN_00e0a750(FNVRange* range); };
float FNVResponse::FUN_00e0a750(FNVRange* range) {
    float displacement = range->value -
        static_cast<float>((range->upper + range->lower) * DAT_01011588);
    float factor;
    if (range->begin < range->end) {
        float difference = range->upper - range->lower;
        float limit = maximum;
        double denominator = double(difference) +
            (limit < difference ? limit : difference);
        if (denominator > 0.0)
            factor = float(1.0 / denominator);
        else
            factor = DAT_010ea608;
    } else {
        factor = range->defaultFactor;
    }
    float amount = factor * displacement;
    if (amount < 0.0f)
        return 0.0f;
    float x2 = amount * amount;
    float x4 = x2 * x2;
    float x8 = x4 * x4;
    float response = static_cast<float>(x2 * DAT_010ea600 + x4 * DAT_01021928 + x8 * DAT_010737c8);
    response *= magnitude;
    return response;
}