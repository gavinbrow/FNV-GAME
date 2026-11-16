struct NiStreamTransfer
{
    void* unk00;
    unsigned int bytesTransferred;
    void* unk08;
    unsigned int (__cdecl *transfer)(NiStreamTransfer*, const void*, unsigned int, unsigned int*, unsigned int);
    __forceinline void TransferData(const void* bytes, unsigned int count, unsigned int initialCount)
    {
        unsigned int bytesTransferred = initialCount;
        this->bytesTransferred += transfer(this, bytes, count, &bytesTransferred, 1);
    }
};

struct NiStreamSerialization
{
    virtual void v00() = 0;
    virtual void v01() = 0;
    virtual void v02() = 0;
    virtual void v03() = 0;
    virtual void v04() = 0;
    virtual void v05() = 0;
    virtual void v06() = 0;
    virtual void v07() = 0;
    virtual void v08() = 0;
    virtual void v09() = 0;
    virtual void v10() = 0;
    virtual void v11() = 0;
    virtual void SavePalette(void*) = 0;
};

struct NiObjectSerialization : NiObject
{
    void FUN_00a89af0(NiStreamSerialization*);
};

struct NiPixelFormatSerialization : NiPixelFormat
{
    void FUN_00a7d1a0(NiStreamSerialization*);
};

struct NiPixelDataSerialization : NiPixelData
{
    void FUN_00a7c670(NiStreamSerialization*);
};

static __forceinline void TransferData(NiStreamSerialization* stream, const void* bytes, unsigned int count, unsigned int initialCount = 4)
{
    NiStreamTransfer* io = *reinterpret_cast<NiStreamTransfer**>(reinterpret_cast<char*>(stream) + 0x250);
    io->TransferData(bytes, count, initialCount);
}

void NiPixelDataSerialization::FUN_00a7c670(NiStreamSerialization* stream)
{
    reinterpret_cast<NiObjectSerialization*>(this)->FUN_00a89af0(stream);
    reinterpret_cast<NiPixelFormatSerialization*>(&m_kPixelFormat)->FUN_00a7d1a0(stream);
    stream->SavePalette(m_spPalette.value);

    TransferData(stream, &m_uiMipmapLevels, sizeof(m_uiMipmapLevels));
    TransferData(stream, &m_uiPixelStride, sizeof(m_uiPixelStride));

    for (unsigned int level = 0; level < m_uiMipmapLevels; ++level)
    {
        TransferData(stream, &m_puiWidth[level], sizeof(unsigned int));
        TransferData(stream, &m_puiHeight[level], sizeof(unsigned int));
        TransferData(stream, &m_puiOffsetInBytes[level], sizeof(unsigned int));
    }

    TransferData(stream, &m_puiOffsetInBytes[m_uiMipmapLevels], sizeof(unsigned int));
    TransferData(stream, &m_uiFaces, sizeof(m_uiFaces));
    const void* pixels = m_pucPixels;
    unsigned int pixelBytes = m_puiOffsetInBytes[m_uiMipmapLevels] * m_uiFaces;
    TransferData(stream, pixels, pixelBytes, 1);
}