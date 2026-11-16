#include <string.h>
void* NiMalloc(unsigned int);
int _NiSprintf(char*, unsigned int, const char*, ...);
struct Matrix3 {
    float m00, m01, m02, m10, m11, m12, m20, m21, m22;
    char* FUN_00a598f0(const char* name);
};
char* Matrix3::FUN_00a598f0(const char* name) {
    unsigned int size = strlen(name) + 128;
    char* result = static_cast<char*>(NiMalloc(size));
    _NiSprintf(result, size, "%s = ((%g,%g,%g),(%g,%g,%g),(%g,%g,%g))", name,
        m00,m01,m02,m10,m11,m12,m20,m21,m22);
    return result;
}
