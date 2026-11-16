extern "C" double DAT_01034208;
extern "C" double DAT_01011590;
struct Vector3 {
    float x, y, z;
    Vector3 operator*(double multiplier) const {
        Vector3 scaled;
        scaled.x = float(x * multiplier);
        scaled.y = float(y * multiplier);
        scaled.z = float(z * multiplier);
        return scaled;
    }
    Vector3 operator*(float multiplier) const {
        Vector3 scaled;
        scaled.x = x * multiplier;
        scaled.y = y * multiplier;
        scaled.z = z * multiplier;
        return scaled;
    }
    Vector3 operator+(const Vector3& right) const {
        Vector3 sum;
        sum.x = x + right.x;
        sum.y = y + right.y;
        sum.z = z + right.z;
        return sum;
    }
};
void __cdecl FUN_00a2b130(float amount, const float* transform, unsigned int unused, Vector3* result)
{
    amount *= DAT_01034208;
    const Vector3* start = reinterpret_cast<const Vector3*>(transform + 13);
    const Vector3* end = reinterpret_cast<const Vector3*>(transform + 16);
    *result = (*start * DAT_01011590) + (*end * amount);
}
