struct TileValue { float FUN_00a011b0(); void FUN_00a012d0(unsigned int, float, bool); };
struct MenuItem { TileValue* FUN_00726070(unsigned int); unsigned int menuId; TileValue* value; void FUN_007ddc20(); };
struct TraitValues { virtual void Unused0(); virtual void Unused1(); virtual void Unused2(); virtual float GetValue(unsigned int); };
extern void* g_011dea3c;
extern double g_01017b70, g_01011590, g_0101ff40, g_01064f50, g_01012060, g_01012070;
float __cdecl FUN_005c5420();
float __cdecl FUN_00404010(float, float);
float __cdecl FUN_004bd510(float, float);
void MenuItem::FUN_007ddc20() {
    float a = FUN_00726070(0x1008)->FUN_00a011b0() * g_01017b70;
    float c = (-a / g_01011590) + FUN_005c5420() * a;
    float d = FUN_00404010(0.0f, ((TraitValues*)((char*)g_011dea3c + 0xa4))->GetValue(0x49));
    float e = g_01064f50 - (d + c) / g_01017b70 * g_0101ff40;
    if (d > g_01012060 && d < g_01012070) d = 1.0f; else d = FUN_004bd510(d, 1.0f);
    value->FUN_00a012d0(0x100f, d, true);
}