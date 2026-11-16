struct FUN_00e53180_Obj {
    float x;
    float y;
    float z;
    float w;
    void FUN_00e53180(const Float4* source);
};
void __cdecl FUN_00e546e0(int a, int b, int c, int d, int count,
                            float** inputs, FUN_00e53180_Obj** outputs)
{
    for (int i = 0; i <= count; ++i) {
        Float4 temporary;
        Float4* converted = reinterpret_cast<Float4* (__cdecl*)(Float4*, int, int, int, int, float)>(&FUN_00e54630)(&temporary, a, b, c, d, (*inputs)[i]);
        (*outputs)[i].FUN_00e53180(converted);
    }
}