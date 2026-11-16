
struct Float4 { float x, y, z, w; };
extern const double DAT_01016978;
void __cdecl FUN_00e54630(Float4* out, int a, int b, int c, int d, float input);
float __cdecl FUN_00e54b20(const Float4* left, const Float4* right);

unsigned char* __cdecl FUN_00e55140(unsigned char* result, int a, int b, int c, int d, int last,
                          Float4** verticesPtr, float** valuesPtr, float** thresholdsPtr)
{
    int index = 0;
    if (last >= 0) {
        float* thresholds = *thresholdsPtr;
        Float4* vertices = *verticesPtr;
        int delta = (char*)*valuesPtr - (char*)thresholds;
        do {
            Float4 lhs = *vertices;
            Float4 rhs;
            FUN_00e54630(&rhs, a, b, d, c, *(float*)((char*)thresholds + delta));
            if (FUN_00e54b20(&lhs, &rhs) > (float)(*thresholds + DAT_01016978)) {
                *result = 0;
                return result;
            }
            ++index;
            ++vertices;
            ++thresholds;
        } while (index <= last);
    }
    *result = 1;
    return result;
}
