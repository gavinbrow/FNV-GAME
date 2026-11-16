struct ShaderMap {
    virtual void Dispose(unsigned int flags);
    void FUN_00b601a0();
};

extern "C" __declspec(dllimport) void __stdcall DeleteCriticalSection(void* criticalSection);

struct ShaderFactoryShutdown : NiD3DShaderFactory {
    void FUN_00e92c40();
    void FUN_00aa05a0();
    void FUN_00e92dc0();
};

void ShaderFactoryShutdown::FUN_00e92dc0() {
    ShaderMap* shaderMap = static_cast<ShaderMap*>(m_pkShaderMap);
    m_vtable = &kVtbl_NiD3DShaderFactory;
    if (shaderMap)
        shaderMap->FUN_00b601a0();

    FUN_00e92c40();

    if (m_pkShaderMap)
        static_cast<ShaderMap*>(m_pkShaderMap)->Dispose(1);
    if (m_pkLibraryMap)
        static_cast<ShaderMap*>(m_pkLibraryMap)->Dispose(1);

    m_pkShaderMap = 0;
    m_pkLibraryMap = 0;
    m_pkRenderer = 0;
    DeleteCriticalSection(m_kShaderMapLock);
    FUN_00aa05a0();
}
