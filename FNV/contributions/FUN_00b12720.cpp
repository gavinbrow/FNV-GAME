extern double __cdecl FUN_00eca190(double value);
struct This : FUN_00b2a180
{
    float FUN_00b12720(const NiPoint3& point);
};
float This::FUN_00b12720(const NiPoint3& point)
{
    float value = Dot(point);
    if (value < -1.0f)
        value = -1.0f;
    if (value > 1.0f)
        value = 1.0f;
    return (float)FUN_00eca190(value);
}
