struct Setting_S {
    float* Float();
};

extern Setting_S DAT_011cdf78;
extern Setting_S DAT_011cdf44;
extern Setting_S DAT_011cde50;
extern Setting_S DAT_011cdce8;

struct FUN_0066ef50_Class {
    double FUN_0066ef50(int a);
};

float __cdecl FUN_00643e40(FUN_0066ef50_Class* actor, int action)
{
    float result = 0.0f;
    switch (action) {
    case 0x13:
        result = (float)((actor->FUN_0066ef50(7) + *DAT_011cdf78.Float()) * *DAT_011cdf44.Float());
        break;
    case 0x14:
        result = (float)((actor->FUN_0066ef50(7) + *DAT_011cde50.Float()) * *DAT_011cdce8.Float());
        break;
    }
    return result;
}
