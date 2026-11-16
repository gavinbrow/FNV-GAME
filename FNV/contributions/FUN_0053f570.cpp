struct NiColorA {
    float r, g, b, a;
    NiColorA(float r, float g, float b, float a);
    NiColorA operator+(const NiColorA& other) const;
    NiColorA operator*(float scalar) const;
};
NiColorA __cdecl operator*(float scalar, const NiColorA& value);
extern "C" float DAT_0101e704;
extern "C" double DAT_0102e430;
float __cdecl FUN_004b1520(float value, float bound);



struct OwnerInterp : Owner {
  void FUN_005345c0(int first, int second, NiColorA* out);
  bool FUN_0053f570(const float* xy, NiColorA* out);
};

bool OwnerInterp::FUN_0053f570(const float* xy, NiColorA* out)
{
    Buf50 data;
    data.FUN_0053a510();
    if (!FUN_0053b550(&data, (int)xy, 0))
        return false;

    NiColorA aVal(0.0f, 0.0f, 0.0f, 0.0f);
    NiColorA b(0.0f, 0.0f, 0.0f, 0.0f);
    NiColorA thirdColor(0.0f, 0.0f, 0.0f, 0.0f);
    float x3 = (float)(FUN_004b1520(xy[0], DAT_0101e704) / DAT_0102e430);
    float y = (float)(FUN_004b1520(xy[1], DAT_0101e704) / DAT_0102e430);
    FUN_005345c0(data.m18, data.m40, &aVal);
    FUN_005345c0(data.m18, data.m44, &b);
    FUN_005345c0(data.m18, data.m48, &thirdColor);

    if (!(*(unsigned char*)&data.m4C) && !(*((unsigned char*)&data.m4C+1))) {
        *out = (((1.0f-x3)*b + x3*aVal) * (1.0f-y)) + y*thirdColor;
    }
    if (!(*(unsigned char*)&data.m4C) && (*((unsigned char*)&data.m4C+1))) {
        *out = (((1.0f-x3)*aVal + x3*thirdColor) * y) + (1.0f-y)*b;
    }
    if ((*(unsigned char*)&data.m4C) && !(*((unsigned char*)&data.m4C+1))) {
        *out = (((1.0f-x3)*aVal + x3*b) * (1.0f-y)) + y*thirdColor;
    }
    if ((*(unsigned char*)&data.m4C) && (*((unsigned char*)&data.m4C+1))) {
        *out = (((1.0f-x3)*thirdColor + x3*aVal) * y) + (1.0f-y)*b;
    }
    return true;
}
