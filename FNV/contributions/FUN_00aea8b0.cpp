
extern "C" const double DAT_010a3be8;
struct FNVRenderInterface_00aea8b0 {
    virtual void __stdcall Function00() = 0;
    virtual void __stdcall Function04() = 0;
    virtual void __stdcall Function08() = 0;
    virtual void __stdcall Function0C() = 0;
    virtual void __stdcall Function10() = 0;
    virtual void __stdcall Function14() = 0;
    virtual void __stdcall Function18() = 0;
    virtual void __stdcall Function1C() = 0;
    virtual void __stdcall Function20() = 0;
    virtual void __stdcall Function24() = 0;
    virtual void __stdcall Function28() = 0;
    virtual void __stdcall Function2C() = 0;
    virtual void __stdcall Function30() = 0;
    virtual void __stdcall ApplyParameters(float a, float b, float c, float d, float e, float f, int enable) = 0;
    virtual void __stdcall ApplyColor(float red, float green, float blue, int enable) = 0;
    virtual void __stdcall Function3C() = 0;
    virtual void __stdcall Function40() = 0;
    virtual void __stdcall Commit() = 0;
};
struct FNVColorRenderer_00aea8b0 {
    unsigned int unknown00;
    float red;
    float blue;
    float green;
    unsigned int unknown10, unknown14, unknown18, unknown1C;
    unsigned int unknown20, unknown24, unknown28, unknown2C;
    unsigned int unknown30, unknown34, unknown38, unknown3C;
    unsigned int unknown40, unknown44;
    FNVRenderInterface_00aea8b0* renderer;
    float scale4c, scale50, scale54;
    float scale58, scale5c, scale60;
    void FUN_00aea8b0();
};
void FNVColorRenderer_00aea8b0::FUN_00aea8b0()
{
    if (renderer) {
        renderer->ApplyColor(
            static_cast<float>(red * DAT_010a3be8),
            static_cast<float>(green * DAT_010a3be8),
            static_cast<float>(blue * DAT_010a3be8), 1);
        renderer->ApplyParameters(scale58, scale60, scale5c,
                                  scale4c, scale54, scale50, 1);
        renderer->Commit();
    }
}
