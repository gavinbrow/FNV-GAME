double __cdecl FUN_00ec6940(double value);

struct FourComponentVector {
    float x, y, z, w;
    __declspec(noinline) FourComponentVector(float a, float b, float c, float d);
    FourComponentVector FUN_00e53440() const;
};
FourComponentVector::FourComponentVector(float a, float b, float c, float d)
    : x(a), y(b), z(c), w(d) {}

FourComponentVector FourComponentVector::FUN_00e53440() const
{
    return FourComponentVector(
        static_cast<float>(FUN_00ec6940(x)),
        static_cast<float>(FUN_00ec6940(y)),
        static_cast<float>(FUN_00ec6940(z)),
        static_cast<float>(FUN_00ec6940(w)));
}