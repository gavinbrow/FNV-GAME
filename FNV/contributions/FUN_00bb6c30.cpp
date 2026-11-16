#include "h_d45a2aa7d3ee.h"

extern MemoryManager g_memoryManager;

class DTPass : public NiRefObject {};
class DTVertexShader : public NiRefObject {};
class DTPixelShader : public NiRefObject {};

struct DistantTreeInstance {
    float x;
    float y;
    float z;
    float w;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    static unsigned int GetMaxCount()
    {
        if (!DAT_012007b8)
            DAT_012007b8 = fnv_particle_shader_renderer_level >= 2 ? 114 : 40;
        return DAT_012007b8;
    }
    static void* operator new[](unsigned int size) { return g_memoryManager.Allocate(size); }
};

struct DistantTreeFogColors {
    NiColorA colors[2];
    DistantTreeFogColors()
    {
        NiColorA* p = colors;
        int count = 1;
        do {
            p->r = 0.0f;
            p->g = 0.0f;
            p->b = 0.0f;
            p->a = 0.0f;
            ++p;
        } while (--count >= 0);
    }
};

struct DistantTreeColor {
    float r;
    float g;
    float b;
    float a;
    __forceinline DistantTreeColor() { r = 0.0f; g = 0.0f; b = 0.0f; a = 0.0f; }
};

struct DTShaderBase : public BSShader {
    DTShaderBase();
    virtual ~DTShaderBase();
};

struct FUN_00bb6c30 : public DTShaderBase {
    NiPointer<DTPass> spPass[2];
    NiPointer<DTVertexShader> spVertexShader[1];
    NiPointer<DTPixelShader> spPixelShader[2];
    NiPointer<NiXenonShaderDeclaration> spDecl;
    DistantTreeFogColors pFogPropA;
    unsigned int uiNumInstances;
    DistantTreeInstance* pInstanceDataA;
    DistantTreeColor pfAmbientColor;
    DistantTreeColor pfDiffuseDir;
    DistantTreeColor pfDiffuseColor;
    DistantTreeColor pEyeVector;
    DistantTreeColor pEyePosition;

    FUN_00bb6c30(NiXenonShaderDeclaration* pDecl);
    virtual ~FUN_00bb6c30();
    virtual BSShader* CreateShader();
};

FUN_00bb6c30::FUN_00bb6c30(NiXenonShaderDeclaration* pDecl)
{
    iShaderType = 25;
    spDecl = pDecl;
    pInstanceDataA = new DistantTreeInstance[DistantTreeInstance::GetMaxCount()];
}

