extern "C" const double DAT_01034208;
extern "C" const double DAT_01011590;
struct Vec3Output { float x,y,z; };
extern "C" void __cdecl FUN_00a27e40(float radians, const float* transform, unsigned int mode, Vec3Output* output) {
    radians = (float)(radians * DAT_01034208);
    Vec3Output offset;
    offset.x = radians * transform[13];
    offset.y = radians * transform[14];
    offset.z = radians * transform[15];
    Vec3Output base;
    base.x = (float)(transform[10] * DAT_01011590);
    base.y = (float)(transform[11] * DAT_01011590);
    base.z = (float)(transform[12] * DAT_01011590);
    Vec3Output sum;
    sum.x = base.x + offset.x;
    sum.y = reinterpret_cast<volatile Vec3Output&>(offset).y + base.y;
    sum.z = base.z + offset.z;
    *output = sum;
}