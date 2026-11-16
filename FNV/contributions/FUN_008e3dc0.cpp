struct RandomOffsetVector {
 float x, y, z;
 void FUN_00416870(float x, float y, float z);
 void FUN_004a0c10();
 RandomOffsetVector FUN_0045bb20(float scale) const;
 RandomOffsetVector FUN_00439e90(const RandomOffsetVector& other) const;
};
float __cdecl FUN_005c5420();
RandomOffsetVector __cdecl FUN_008e3dc0(RandomOffsetVector origin, float minimum, float maximum, bool randomizeZ)
{
 float d;
 float c;
 c = FUN_005c5420();
 d = FUN_005c5420();
 float f = 0.0f;
 if (randomizeZ) f = FUN_005c5420();
 RandomOffsetVector a;
 a.FUN_00416870(c, d, f);
 a.FUN_004a0c10();
 float e = FUN_005c5420();
 float b = (minimum + maximum) * e;
 if (b < maximum) b = maximum;
 a = origin.FUN_00439e90(a.FUN_0045bb20(b));
 return a;
}