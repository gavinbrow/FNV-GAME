float __cdecl FUN_0066dc70(int value);
float* __fastcall FUN_00403e20(void* object);
extern unsigned char DAT_011d5f88;

float __cdecl FUN_0066dca0(int value, bool unscaled)
{
    float baseValue = FUN_0066dc70(value);
    if (!unscaled)
    {
        return baseValue * *FUN_00403e20(&DAT_011d5f88);
    }
    else
    {
        return baseValue;
    }
}