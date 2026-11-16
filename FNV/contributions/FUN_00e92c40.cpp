struct ShaderLibrary_92c40 { const char* FUN_00d47a30(); };
struct ReferenceObject_92c40 {
    virtual void Reserved();
    virtual void Release();
    volatile long referenceCount;
};
struct LibraryMap_92c40 {
    void FUN_00e91fd0(const char*);
    void FUN_00e6e630(void**, void**, ReferenceObject_92c40**);
    void FUN_00b601a0();
};
struct FUN_00e92c40_shell : NiD3DShaderFactory {
    ShaderLibrary_92c40* FUN_00e92b50();
    void FUN_00e92c40();
};
void FUN_00e92c40_shell::FUN_00e92c40() {
    if (!m_pkLibraryMap) return;
    ShaderLibrary_92c40* current = FUN_00e92b50();
    if (current) {
        do {
            ((LibraryMap_92c40*)m_pkLibraryMap)->FUN_00e91fd0(current->FUN_00d47a30());
            if (!m_pkLibraryMap || !m_kLibraryIter) break;
            ReferenceObject_92c40* next = 0;
            void* scratch;
            ((LibraryMap_92c40*)m_pkLibraryMap)->FUN_00e6e630(&m_kLibraryIter, &scratch, &next);
            ReferenceObject_92c40* savedNext = *(ReferenceObject_92c40* volatile*)&next;
            if (savedNext && InterlockedDecrement(&savedNext->referenceCount) == 0)
                savedNext->Release();
            current = (ShaderLibrary_92c40*)savedNext;
        } while (current);
    }
    ((LibraryMap_92c40*)m_pkLibraryMap)->FUN_00b601a0();
}