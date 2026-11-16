struct NiBinaryStreamView {
    typedef unsigned int (__cdecl *READFN)(NiBinaryStreamView*, void*, unsigned int, unsigned int*, unsigned int);
    void* m_vtable;
    unsigned int m_uiAbsoluteCurrentPos;
    unsigned int m_uiBufferSize;
    READFN m_pfnRead;
    __forceinline unsigned int BinaryRead(void* pvBuffer, unsigned int uiTotalBytes, unsigned int* puiComponentSizes, unsigned int uiNumComponents)
    {
        unsigned int uiBytesRead = m_pfnRead(this, pvBuffer, uiTotalBytes, puiComponentSizes, uiNumComponents);
        m_uiAbsoluteCurrentPos += uiBytesRead;
        return uiBytesRead;
    }
};

struct NiStreamView {
    __forceinline NiBinaryStreamView* Input() { return *reinterpret_cast<NiBinaryStreamView**>(reinterpret_cast<char*>(this) + 0x250); }
    void FUN_00a64160(unsigned int linkId);
};

struct NiExtraDataView {
    void* m_vtable;
    unsigned int m_uiRefCount;
    char* m_pcName;
    unsigned int m_uiNumEntries;
    unsigned int* m_pLinkIds;
    unsigned int m_uiTail;
    void FUN_00a7b2c0(NiStreamView& kStream);
    void FUN_00a939d0(NiStreamView& kStream);
};

template <class T>
__forceinline void NiBinaryStreamLoad(NiBinaryStreamView& is, T* pValue, unsigned int uiNumEls = 1)
{
    unsigned int uiSize = sizeof(T);
    is.BinaryRead(pValue, sizeof(T) * uiNumEls, &uiSize, 1);
}
template <class T>
__forceinline void NiStreamLoadBinary(NiStreamView& kStream, T& value)
{
    NiBinaryStreamLoad(*kStream.Input(), &value, 1);
}

void NiExtraDataView::FUN_00a939d0(NiStreamView& kStream)
{
    FUN_00a7b2c0(kStream);
    NiStreamLoadBinary(kStream, m_uiNumEntries);
    for (unsigned int i = 0; i < m_uiNumEntries; ++i)
        kStream.FUN_00a64160(m_pLinkIds[i]);
    NiStreamLoadBinary(kStream, m_uiTail);
}