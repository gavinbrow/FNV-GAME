
struct RendererApi {
    virtual void UnknownSlot00() = 0;
    virtual void UnknownSlot01() = 0;
    virtual void UnknownSlot02() = 0;
    virtual void UnknownSlot03() = 0;
    virtual void UnknownSlot04() = 0;
    virtual void UnknownSlot05() = 0;
    virtual void UnknownSlot06() = 0;
    virtual void UnknownSlot07() = 0;
    virtual void UnknownSlot08() = 0;
    virtual void UnknownSlot09() = 0;
    virtual void UnknownSlot10() = 0;
    virtual void UnknownSlot11() = 0;
    virtual void UnknownSlot12() = 0;
    virtual void UnknownSlot13() = 0;
    virtual void UnknownSlot14() = 0;
    virtual void UnknownSlot15() = 0;
    virtual void UnknownSlot16() = 0;
    virtual void UnknownSlot17() = 0;
    virtual void UnknownSlot18() = 0;
    virtual void UnknownSlot19() = 0;
    virtual void UnknownSlot20() = 0;
    virtual void UnknownSlot21() = 0;
    virtual void UnknownSlot22() = 0;
    virtual void UnknownSlot23() = 0;
    virtual void UnknownSlot24() = 0;
    virtual void UnknownSlot25() = 0;
    virtual void UnknownSlot26() = 0;
    virtual void UnknownSlot27() = 0;
    virtual void UnknownSlot28() = 0;
    virtual void UnknownSlot29() = 0;
    virtual void UnknownSlot30() = 0;
    virtual void SetPixelProgram(unsigned int program, unsigned int option) = 0;
    virtual void UnknownSlot32() = 0;
    virtual void UnknownSlot33() = 0;
    virtual void UnknownSlot34() = 0;
    virtual void SetVertexProgram(unsigned int program, unsigned int option) = 0;
    virtual void UnknownSlot36() = 0;
    virtual void UnknownSlot37() = 0;
    virtual void UnknownSlot38() = 0;
    virtual void SetRenderEntry(unsigned int entry, unsigned int option) = 0;
    virtual void UnknownSlot40() = 0;
    virtual void UnknownSlot41() = 0;
    virtual void UnknownSlot42() = 0;
    virtual void SetRenderValue(unsigned int value, unsigned int option) = 0;
    virtual void UnknownSlot44() = 0;
    virtual void UnknownSlot45() = 0;
    virtual void UnknownSlot46() = 0;
    virtual void UnknownSlot47() = 0;
    virtual void SetTextureStageState(unsigned int stage, unsigned int state, unsigned int value, unsigned int flags) = 0;
};
struct ShaderProgram {
    virtual void UnknownSlot00() = 0;
    virtual void UnknownSlot01() = 0;
    virtual void UnknownSlot02() = 0;
    virtual void UnknownSlot03() = 0;
    virtual void UnknownSlot04() = 0;
    virtual void UnknownSlot05() = 0;
    virtual void UnknownSlot06() = 0;
    virtual void UnknownSlot07() = 0;
    virtual void UnknownSlot08() = 0;
    virtual void UnknownSlot09() = 0;
    virtual void UnknownSlot10() = 0;
    virtual void UnknownSlot11() = 0;
    virtual void UnknownSlot12() = 0;
    virtual void UnknownSlot13() = 0;
    virtual void UnknownSlot14() = 0;
    virtual void UnknownSlot15() = 0;
    virtual void UnknownSlot16() = 0;
    virtual void UnknownSlot17() = 0;
    virtual void UnknownSlot18() = 0;
    virtual void UnknownSlot19() = 0;
    virtual void UnknownSlot20() = 0;
    virtual void UnknownSlot21() = 0;
    virtual void UnknownSlot22() = 0;
    virtual void UnknownSlot23() = 0;
    virtual void UnknownSlot24() = 0;
    virtual void UnknownSlot25() = 0;
    virtual void UnknownSlot26() = 0;
    virtual void UnknownSlot27() = 0;
    virtual void UnknownSlot28() = 0;
    virtual void UnknownSlot29() = 0;
    virtual void UnknownSlot30() = 0;
    virtual unsigned int GetPixelProgram() = 0;
    virtual void UnknownSlot32() = 0;
    virtual unsigned int GetVertexProgram() = 0;
};
struct ShaderConstantMap {
    virtual void UnknownSlot00() = 0;
    virtual void UnknownSlot01() = 0;
    virtual void UnknownSlot02() = 0;
    virtual void UnknownSlot03() = 0;
    virtual void UnknownSlot04() = 0;
    virtual void UnknownSlot05() = 0;
    virtual void UnknownSlot06() = 0;
    virtual void UnknownSlot07() = 0;
    virtual void UnknownSlot08() = 0;
    virtual void UnknownSlot09() = 0;
    virtual void UnknownSlot10() = 0;
    virtual void UnknownSlot11() = 0;
    virtual void UnknownSlot12() = 0;
    virtual void UnknownSlot13() = 0;
    virtual void UnknownSlot14() = 0;
    virtual void UnknownSlot15() = 0;
    virtual void UnknownSlot16() = 0;
    virtual void UnknownSlot17() = 0;
    virtual void UnknownSlot18() = 0;
    virtual void UnknownSlot19() = 0;
    virtual void UnknownSlot20() = 0;
    virtual void UnknownSlot21() = 0;
    virtual void UnknownSlot22() = 0;
    virtual void UnknownSlot23() = 0;
    virtual void UnknownSlot24() = 0;
    virtual void UnknownSlot25() = 0;
    virtual void UnknownSlot26() = 0;
    virtual void UnknownSlot27() = 0;
    virtual void UnknownSlot28() = 0;
    virtual void UnknownSlot29() = 0;
    virtual void ApplyConstants(void* shader, unsigned int p1, unsigned int p2, unsigned int p3, unsigned int p4, unsigned int p5, unsigned int p6, unsigned int p7, unsigned int p8, unsigned int p9, unsigned int flags) = 0;
};
struct TextureStageParameter {
    unsigned int id;
    unsigned int setting04;
    unsigned int setting08;
    unsigned int setting0c;
    FUN_00e89060_shell* state;
};
struct PassUpdate : NiD3DPass {
    unsigned int FUN_00e7f990(unsigned int p1, unsigned int p2, unsigned int p3,
        unsigned int p4, unsigned int p5, unsigned int p6, unsigned int p7,
        unsigned int p8, unsigned int p9);
};
unsigned int PassUpdate::FUN_00e7f990(unsigned int p1, unsigned int p2,
    unsigned int p3, unsigned int p4, unsigned int p5, unsigned int p6,
    unsigned int p7, unsigned int p8, unsigned int p9)
{
    ShaderProgram* pixel = reinterpret_cast<ShaderProgram*>(m_spPixelShader.m_pObject);
    if (pixel) {
        reinterpret_cast<RendererApi*>(DAT_0126f728)->SetPixelProgram(pixel->GetPixelProgram(), 0);
        ShaderConstantMap* constants =
            reinterpret_cast<ShaderConstantMap*>(m_spPixelConstantMap.m_pObject);
        if (constants)
            constants->ApplyConstants(m_spPixelShader.m_pObject,p1,p2,p3,p4,p5,p6,p7,p8,p9,0);
    } else {
        reinterpret_cast<RendererApi*>(DAT_0126f728)->SetPixelProgram(0, 0);
    }
    ShaderProgram* vertex = reinterpret_cast<ShaderProgram*>(m_spVertexShader.m_pObject);
    if (vertex) {
        reinterpret_cast<RendererApi*>(DAT_0126f728)->SetVertexProgram(vertex->GetVertexProgram(), 0);
        ShaderConstantMap* constants =
            reinterpret_cast<ShaderConstantMap*>(m_spVertexConstantMap.m_pObject);
        if (constants)
            constants->ApplyConstants(m_spVertexShader.m_pObject,p1,p2,p3,p4,p5,p6,p7,p8,p9,0);
        for (unsigned int stageIndex = 0; stageIndex < (unsigned int)DAT_011bf558; ++stageIndex) {
            reinterpret_cast<RendererApi*>(DAT_0126f728)->SetTextureStageState(stageIndex,11,stageIndex,0);
            unsigned int texcoordFlags = 0;
            if (stageIndex < m_uiStageCount) {
                NiD3DTextureStage* stage = m_kStages.m_pBase[stageIndex].m_pObject;
                if (stage) {
                    TextureStageParameter* info = reinterpret_cast<TextureStageParameter*>(stage);
                    if (info->state) {
                        unsigned int value = 0;
                        bool initialized = false;
                        if (info->state->FUN_00e89060(24,reinterpret_cast<int*>(&value),&initialized) && (value & 0x100))
                            texcoordFlags = 0x100;
                    }
                }
            }
            reinterpret_cast<RendererApi*>(DAT_0126f728)->SetTextureStageState(stageIndex,24,texcoordFlags,0);
        }
    } else {
        reinterpret_cast<RendererApi*>(DAT_0126f728)->SetVertexProgram(0,0);
        unsigned int* context = reinterpret_cast<unsigned int*>(p4);
        if (!context) {
            if (p3)
                context = reinterpret_cast<unsigned int*>(*reinterpret_cast<unsigned int*>(p3 + 0x28));
            else {
                unsigned int ctx = *reinterpret_cast<unsigned int*>(p1 + 0xb8);
                context = reinterpret_cast<unsigned int*>(*reinterpret_cast<unsigned int*>(ctx + 0x34));
            }
        }
        if (context[3])
            reinterpret_cast<RendererApi*>(DAT_0126f728)->SetRenderEntry(context[3],0);
        else
            reinterpret_cast<RendererApi*>(DAT_0126f728)->SetRenderValue(context[4],0);
    }
    return 0;
}
