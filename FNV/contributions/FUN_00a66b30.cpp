struct NiBoundProxy {
    void FUN_00a7ee30(unsigned int vertexCount, NiPoint3* vertices);
};
struct NiGeometryDataRecovered : NiGeometryData {
    virtual void ReservedGeometryMethod27();
    virtual void ReservedGeometryMethod28();
    virtual void ReservedGeometryMethod29();
    virtual void ReservedGeometryMethod30();
    virtual void ReservedGeometryMethod31();
    virtual void ReservedGeometryMethod32();
    virtual void ReservedGeometryMethod33();
    virtual void ReservedGeometryMethod34();
    virtual void ReservedGeometryMethod35();
    virtual unsigned short GetActualVertexCount();
    void FUN_00a66b30(unsigned short vertexCount,
                      NiPoint3* vertices, NiPoint3* normals,
                      NiColorA* colors, NiPoint2* textureCoords,
                      unsigned short textureSetCount, unsigned short normalBinormalMethod);
};
void NiGeometryDataRecovered::FUN_00a66b30(
    unsigned short vertexCount, NiPoint3* vertices, NiPoint3* normals,
    NiColorA* colors, NiPoint2* textureCoords,
    unsigned short textureSetCount, unsigned short normalBinormalMethod)
{
    m_usVertices = vertexCount;
    m_pkVertex = vertices;
    m_pkNormal = normals;
    unsigned short actualCount = GetActualVertexCount();
    if (actualCount != 0 && m_pkVertex != 0)
        reinterpret_cast<NiBoundProxy*>(&m_kBound)->FUN_00a7ee30(actualCount, m_pkVertex);
    m_pkColor = colors;
    m_pkTexture = textureCoords;
    m_usDataFlags = (m_usDataFlags & 0x0ffe) | (textureSetCount & 1) | normalBinormalMethod;
}