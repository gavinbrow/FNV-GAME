struct Vec3 {
    float x, y, z;
    Vec3() {}
    Vec3(float inX,float inY,float inZ) : x(inX),y(inY),z(inZ) {}
};
struct Spline {
    void __thiscall FUN_00a526b0(float time, float* output, unsigned int count,
        unsigned int offset, unsigned int index, float scale, float bias);
};
struct Interpolator {
    unsigned int unk00;
    unsigned int unk04;
    float lastTime;
    float startTime;
    float endTime;
    Spline* spline;
    unsigned int componentOffset;
    Vec3 lastValue;
    unsigned int controlPointIndex;
    float scale;
    float bias;

    bool __thiscall FUN_00a51280(float time, unsigned int unused, Vec3* out);
};
bool Interpolator::FUN_00a51280(float time, unsigned int unused, Vec3* out)
{
    if (lastTime == time) {
        *out = lastValue;
        return true;
    }
    if (controlPointIndex != 0xffff) {
        float samples[4];
        float normalized = (time - startTime) / (endTime - startTime);
        spline->FUN_00a526b0(normalized, samples, 3, componentOffset,
            controlPointIndex, scale, bias);
        Vec3 updated(samples[0], samples[1], samples[2]);
        lastValue = updated;
    }
    *out = lastValue;
    lastTime = time;
    return true;
}