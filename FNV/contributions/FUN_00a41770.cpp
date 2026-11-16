struct FNVBinaryInput {
    void* m_vtable;
    unsigned int m_uiAbsoluteCurrentPos;
    unsigned int (__cdecl *m_pfnRead)(FNVBinaryInput*, const void*, unsigned int, unsigned int*, unsigned int);
    unsigned int Read(const void* data, unsigned int bytes, unsigned int* elementSize, unsigned int elementCount)
    {
        unsigned int bytesRead = m_pfnRead(this, data, bytes, elementSize, elementCount);
        m_uiAbsoluteCurrentPos += bytesRead;
        return bytesRead;
    }
};
template <class T>
inline unsigned int FNVReadElements(FNVBinaryInput& stream, const T* data, unsigned int count)
{
    unsigned int elementSize = sizeof(T);
    return stream.Read(data, count * elementSize, &elementSize, 1);
}
void __cdecl FUN_00a41770(NiStreamM* context, const unsigned int* data, unsigned int count)
{
    FNVBinaryInput* stream = reinterpret_cast<FNVBinaryInput*>(context->unk24C);
    FNVReadElements(*stream, data, count);
}
