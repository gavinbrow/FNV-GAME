struct FUN_00b0cff0_class {
    float x;
    float y;
    float z;
    NiPoint3* __thiscall FUN_00b0cff0(NiPoint3* output, float factor);
};
NiPoint3* FUN_00b0cff0_class::FUN_00b0cff0(NiPoint3* output, float factor) {
    float z = factor * this->x;
    float x = factor * this->y;
    float y = factor * this->z;
    output->x = z;
    output->y = x;
    output->z = y;
    return output;
}
