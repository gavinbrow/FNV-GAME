
struct S_00c22530_BinaryStream : NiBinaryStream {
    unsigned int (__cdecl *m_readElement)(S_00c22530_BinaryStream*, void*, unsigned int, unsigned int*, unsigned int);
};
struct S_00c22530_Stream : NiStream {
    S_00c22530_BinaryStream* m_reader;
};
inline void S_00c22530_BinaryRead(S_00c22530_BinaryStream* b, void* p) {
    unsigned int size = 4;
    unsigned int got = b->m_readElement(b, p, 4, &size, 1);
    b->m_uiAbsoluteCurrentPos += got;
}
inline void S_00c22530_ReadFloat(S_00c22530_Stream& s, float& f) {
    S_00c22530_BinaryRead(s.m_reader, &f);
}
struct S_00c22530_Emitter : NiPSysEmitter {
    void FUN_00c31950(NiStream& stream);
    void FUN_00c22530(S_00c22530_Stream& stream);
};
void S_00c22530_Emitter::FUN_00c22530(S_00c22530_Stream& stream) {
    FUN_00c31950(stream);
    S_00c22530_ReadFloat(stream, m_fSpeed);
    S_00c22530_ReadFloat(stream, m_fSpeedVar);
    S_00c22530_ReadFloat(stream, m_fDeclination);
    S_00c22530_ReadFloat(stream, m_fDeclinationVar);
    S_00c22530_ReadFloat(stream, m_fPlanarAngle);
    S_00c22530_ReadFloat(stream, m_fPlanarAngleVar);
    m_kInitialColor.LoadBinary(stream);
    S_00c22530_ReadFloat(stream, m_fInitialRadius);
    S_00c22530_ReadFloat(stream, m_fRadiusVar);
    S_00c22530_ReadFloat(stream, m_fLifeSpan);
    S_00c22530_ReadFloat(stream, m_fLifeSpanVar);
}