
struct NiBinaryStream;
typedef unsigned int (__cdecl *BinaryWriteProc)(NiBinaryStream*, const void*, unsigned int, const void*, unsigned int);
struct NiBinaryStream { 
    void* m_pVtbl;
    unsigned int m_uiWriteOffset;
    void* m_pReadProc;
    BinaryWriteProc m_pWriteProc;
    
void WriteSpawnFlag(const bool& onDeath) {
    unsigned int count = 1;
    unsigned int amount = m_pWriteProc(this, &onDeath, 1, &count, 1);
    m_uiWriteOffset += amount;
}
};
struct NiPSysModifierSaveBase { void FUN_00c31950(NiStream* stream); };
struct FUN_00c2f260_shell { void FUN_00c2f260(NiStream* stream); };
void FUN_00c2f260_shell::FUN_00c2f260(NiStream* stream) {
    reinterpret_cast<NiPSysModifierSaveBase*>(this)->FUN_00c31950(stream);
    NiPSysAgeDeathModifierClone* modifier = reinterpret_cast<NiPSysAgeDeathModifierClone*>(this);
    bool spawnOnDeath = modifier->m_bSpawnOnDeath;
    NiBinaryStream* output = *reinterpret_cast<NiBinaryStream**>(reinterpret_cast<char*>(stream) + 0x250);
    output->WriteSpawnFlag(spawnOnDeath);
    typedef void (__thiscall *WriteLinkProc)(NiStream*, NiPSysSpawnModifier*);
    WriteLinkProc* methods = *reinterpret_cast<WriteLinkProc**>(stream);
    methods[12](stream, modifier->m_pkSpawnModifier);
}
