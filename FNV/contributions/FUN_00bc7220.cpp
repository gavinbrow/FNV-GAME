#include "h_ed402c7d2c33.h"

struct NiD3DPassRelease {
    void FUN_00e80190();
};

inline NiPointer<NiD3DPass>::~NiPointer() {
    NiD3DPass* pass = m_pObject;
    if (pass) {
        unsigned int* referenceCount = (unsigned int*)((char*)pass + 0x64);
        if (--*referenceCount == 0) {
            ((NiD3DPassRelease*)pass)->FUN_00e80190();
        }
    }
}
inline NiPointer<NiD3DVertexShader>::~NiPointer() {
    if (m_pObject) m_pObject->DecRefCount();
}
inline NiPointer<NiD3DPixelShader>::~NiPointer() {
    if (m_pObject) m_pObject->DecRefCount();
}
inline NiPointer<NiXenonShaderDeclaration>::~NiPointer() {
    if (m_pObject) m_pObject->DecRefCount();
}

__forceinline BSShaderNoLighting::~BSShaderNoLighting() {
    for (unsigned int i = 0; i < 30; ++i) {
        NiD3DPass* pass = spPass[i].m_pObject;
        if (pass) {
            unsigned int* referenceCount = (unsigned int*)((char*)pass + 0x64);
            if (--*referenceCount == 0) {
                ((NiD3DPassRelease*)pass)->FUN_00e80190();
            }
            spPass[i].m_pObject = 0;
        }
    }

    for (unsigned int i = 0; i < 28; ++i) {
        NiD3DVertexShader* vertex = spVertexShader[i].m_pObject;
        if (vertex) {
            vertex->DecRefCount();
            spVertexShader[i].m_pObject = 0;
        }
    }

    for (unsigned int i = 0; i < 7; ++i) {
        NiD3DPixelShader* pixel = spPixelShader[i].m_pObject;
        if (pixel) {
            pixel->DecRefCount();
            spPixelShader[i].m_pObject = 0;
        }
    }

    if (pBonesEntry.m_pObject) { pBonesEntry.m_pObject->DecRefCount(); pBonesEntry.m_pObject = 0; }
    if (spDecl.m_pObject) { spDecl.m_pObject->DecRefCount(); spDecl.m_pObject = 0; }
    if (spDeclVc.m_pObject) { spDeclVc.m_pObject->DecRefCount(); spDeclVc.m_pObject = 0; }
    if (spDeclTexVc.m_pObject) { spDeclTexVc.m_pObject->DecRefCount(); spDeclTexVc.m_pObject = 0; }
    if (spDeclN.m_pObject) { spDeclN.m_pObject->DecRefCount(); spDeclN.m_pObject = 0; }
    if (spDeclVcN.m_pObject) { spDeclVcN.m_pObject->DecRefCount(); spDeclVcN.m_pObject = 0; }
    if (spDeclTexVcN.m_pObject) { spDeclTexVcN.m_pObject->DecRefCount(); spDeclTexVcN.m_pObject = 0; }
    if (spSkinDecl.m_pObject) { spSkinDecl.m_pObject->DecRefCount(); spSkinDecl.m_pObject = 0; }
    if (spSkinDeclVc.m_pObject) { spSkinDeclVc.m_pObject->DecRefCount(); spSkinDeclVc.m_pObject = 0; }
    if (spSkinDeclTexVc.m_pObject) { spSkinDeclTexVc.m_pObject->DecRefCount(); spSkinDeclTexVc.m_pObject = 0; }
    if (spSkinDeclN.m_pObject) { spSkinDeclN.m_pObject->DecRefCount(); spSkinDeclN.m_pObject = 0; }
    if (spSkinDeclVcN.m_pObject) { spSkinDeclVcN.m_pObject->DecRefCount(); spSkinDeclVcN.m_pObject = 0; }
    pParticleSubTextureOffsetEntry = 0;
}

void __fastcall FUN_00bc7220(BSShaderNoLighting* shader) {
    shader->BSShaderNoLighting::~BSShaderNoLighting();
}
