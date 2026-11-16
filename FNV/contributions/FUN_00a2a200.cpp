struct Quaternion {
    float x;
    float y;
    float z;
    float w;
    Quaternion& operator*=(float scalar) {
        x *= scalar;
        y *= scalar;
        z *= scalar;
        w *= scalar;
        return *this;
    }
    Quaternion operator+(const Quaternion& other) const {
        Quaternion result = *this;
        result.x += other.x;
        result.y += other.y;
        result.z += other.z;
        result.w += other.w;
        return result;
    }
};
struct QuaternionKey {
    float time;
    Quaternion value;
};
void __cdecl FUN_00a2a200(float interpolation, const QuaternionKey* first, const QuaternionKey* second, Quaternion* output)
{
    float inverse = 1.0f - interpolation;
    Quaternion left = first->value;
    Quaternion right = second->value;
    left *= inverse;
    right *= interpolation;
    *output = right + left;
}