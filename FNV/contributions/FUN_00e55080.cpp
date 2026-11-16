struct Vector4 {
    float x;
    float y;
    float z;
    float w;
};
extern const double DAT_010290f8;
void __cdecl FUN_00e54630(Vector4* result, int a, int b, int c, int d, float value);
float __cdecl FUN_00e54b20(const Vector4* a, const Vector4* b);

unsigned char* __cdecl FUN_00e55080(
    unsigned char* result, int a, int b, int c, int d,
    int count, const Vector4** points, const float** weights, float threshold)
{
    *result = 1;
    if (count >= 0) {
        double limit = threshold * DAT_010290f8;
        const float* weight = *weights;
        const Vector4* point = *points;
        int remaining = count + 1;
        do {
            Vector4 v = *point;
            Vector4 transformed;
            FUN_00e54630(&transformed, a, b, d, c, *weight);
            if (FUN_00e54b20(&v, &transformed) > limit) {
                *result = 0;
            }
            ++point;
            ++weight;
        } while (--remaining);
    }
    return result;
}