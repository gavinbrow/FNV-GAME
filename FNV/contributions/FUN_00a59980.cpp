struct TransformRecord {
    float unk00;
    float unk04;
    float unk08;
    float unk0C;
    float unk10;
    float unk14;
    float unk18;
    float unk1C;
    float unk20;
    bool __thiscall FUN_00a58990(unsigned int parameter, float* result);
    void __thiscall FUN_00a58b00(unsigned int parameter, float* result);
    void __thiscall FUN_00a59980(unsigned int parameter, float* output);
};

void TransformRecord::FUN_00a59980(unsigned int parameter, float* output)
{
    TransformRecord copy = *this;
    float intermediate[2];
    bool negate = copy.FUN_00a58990(parameter, intermediate);
    copy.FUN_00a58b00(parameter, intermediate);
    output[0] = copy.unk00;
    output[1] = copy.unk0C;
    output[2] = copy.unk18;
    output[3] = copy.unk04;
    output[4] = copy.unk10;
    output[5] = copy.unk1C;
    if (negate) {
        output[6] = -copy.unk08;
        output[7] = -copy.unk14;
        output[8] = -copy.unk20;
    } else {
        output[6] = copy.unk08;
        output[7] = copy.unk14;
        output[8] = copy.unk20;
    }
}
