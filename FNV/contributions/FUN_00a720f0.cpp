struct FUN_00a720f0_shell : public NiLight { void FUN_00a720f0(NiStream& stream); };
struct FUN_00a68f80_shell : public NiDynamicEffect { void FUN_00a68f80(NiStream&); };
struct NiColorSaveHelper { void SaveBinary(NiStream&); };
struct NiBinaryStreamWriteShell : public NiBinaryStream {
    unsigned int BinaryWrite(void* data, unsigned int size) {
        unsigned int componentSizes[1] = { size };
        unsigned int written = m_pfnWrite(this, data, size, componentSizes, 1);
        m_uiAbsoluteCurrentPos += written;
        return written;
    }
};
void FUN_00a720f0_shell::FUN_00a720f0(NiStream& stream) {
    reinterpret_cast<FUN_00a68f80_shell*>(this)->FUN_00a68f80(stream);
    reinterpret_cast<NiBinaryStreamWriteShell*>(stream.m_pkOstr)->BinaryWrite(&m_fDimmer, 4);
    reinterpret_cast<NiColorSaveHelper*>(&m_kAmb)->SaveBinary(stream);
    reinterpret_cast<NiColorSaveHelper*>(&m_kDiff)->SaveBinary(stream);
    reinterpret_cast<NiColorSaveHelper*>(&m_kSpec)->SaveBinary(stream);
}