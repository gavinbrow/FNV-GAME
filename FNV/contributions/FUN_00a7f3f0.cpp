#include <math.h>

struct NiPt3 {
    float x, y, z;
    NiPt3() {}
    NiPt3(float ax, float ay, float az) : x(ax), y(ay), z(az) {}
    NiPt3 operator-(const NiPt3& o) const { return NiPt3(x - o.x, y - o.y, z - o.z); }
    NiPt3 operator+(const NiPt3& o) const { return NiPt3(x + o.x, y + o.y, z + o.z); }
    NiPt3 operator*(float s) const { return NiPt3(x * s, y * s, z * s); }
    float SqrLength() const { return x * x + y * y + z * z; }
};

extern const float kSphereEpsilon;

struct Sphere {
    NiPt3 center;
    float radius;
    void FUN_00a7f3f0(const Sphere& other);
};

void Sphere::FUN_00a7f3f0(const Sphere& other)
{
    NiPt3 d = center - other.center;
    float distSq = d.SqrLength();
    float r = other.radius - radius;
    float rSq = r * r;
    float dist;
    if (r >= 0.0f) {
        if (rSq >= distSq) {
            center = other.center;
            radius = other.radius;
            return;
        }
        dist = sqrtf(distSq);
    if (dist > kSphereEpsilon) {
        float t = (dist - r) / (dist * 2.0f);
        center = other.center + d * t;
    }
    radius = (dist + other.radius + radius) * 0.5;
        return;
    }
    if (!(rSq < distSq)) return;
    dist = sqrtf(distSq);
    if (dist > kSphereEpsilon) {
        float t = (dist - r) / (dist * 2.0f);
        center = other.center + d * t;
    }
    radius = (dist + other.radius + radius) * 0.5;
}
