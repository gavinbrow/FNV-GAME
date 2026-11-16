#include <math.h>
struct Point3 {
    float x, y, z;
    float Length() const { return sqrtf(x*x + y*y + z*z); }
};
extern char* DAT_011f917c;
struct ImageSpaceDistanceEffect {
    void FUN_00b8b0d0(float strength, int mode, float duration, float nearDistance, float farDistance);
    void FUN_00b8b8d0(float strength, int mode, float duration, const Point3* position);
};
void ImageSpaceDistanceEffect::FUN_00b8b8d0(float strength, int mode, float duration, const Point3* position) {
    const Point3 worldPosition = *reinterpret_cast<const Point3*>(DAT_011f917c + 0x8c);
    const volatile Point3 sample = *position;
    const Point3 delta = { sample.x - worldPosition.x, sample.y - worldPosition.y, sample.z - worldPosition.z };
    const float distance = delta.Length();
    FUN_00b8b0d0(strength, mode, duration, distance, distance);
}