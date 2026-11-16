class NiStream;

struct NiBinaryStream
{
    int unk00;
    unsigned int m_uiAbsoluteCurrentPos;
    unsigned int (*m_pfnRead)(NiBinaryStream* pkThis, void* pvBuffer, unsigned int uiBytes,
        unsigned int* puiComponentSizes, unsigned int uiNumComponents);

    unsigned int BinaryRead(void* pvBuffer, unsigned int uiTotalBytes,
        unsigned int* puiComponentSizes, unsigned int uiNumComponents)
    {
        unsigned int uiBytesRead = m_pfnRead(this, pvBuffer, uiTotalBytes, puiComponentSizes, uiNumComponents);
        m_uiAbsoluteCurrentPos += uiBytesRead;
        return uiBytesRead;
    }
};

class NiStream
{
public:
    int unk00; int unk04; int unk08; int unk0C; int unk10; int unk14; int unk18; int unk1C; int unk20; int unk24; int unk28; int unk2C; int unk30; int unk34; int unk38; int unk3C; int unk40; int unk44; int unk48; int unk4C; int unk50; int unk54; int unk58; int unk5C; int unk60; int unk64; int unk68; int unk6C; int unk70; int unk74; int unk78; int unk7C; int unk80; int unk84; int unk88; int unk8C; int unk90; int unk94; int unk98; int unk9C; int unkA0; int unkA4; int unkA8; int unkAC; int unkB0; int unkB4; int unkB8; int unkBC; int unkC0; int unkC4; int unkC8; int unkCC; int unkD0; int unkD4;
    unsigned int m_uiNifFileVersion;
    int unk0DC; int unk0E0; int unk0E4; int unk0E8; int unk0EC; int unk0F0; int unk0F4; int unk0F8; int unk0FC; int unk100; int unk104; int unk108; int unk10C; int unk110; int unk114; int unk118; int unk11C; int unk120; int unk124; int unk128; int unk12C; int unk130; int unk134; int unk138; int unk13C; int unk140; int unk144; int unk148; int unk14C; int unk150; int unk154; int unk158; int unk15C; int unk160; int unk164; int unk168; int unk16C; int unk170; int unk174; int unk178; int unk17C; int unk180; int unk184; int unk188; int unk18C; int unk190; int unk194; int unk198; int unk19C; int unk1A0; int unk1A4; int unk1A8; int unk1AC; int unk1B0; int unk1B4; int unk1B8; int unk1BC; int unk1C0; int unk1C4; int unk1C8; int unk1CC; int unk1D0; int unk1D4; int unk1D8; int unk1DC; int unk1E0; int unk1E4;
    int unk1E8;
    int unk1EC; int unk1F0; int unk1F4; int unk1F8; int unk1FC; int unk200; int unk204; int unk208; int unk20C; int unk210; int unk214; int unk218; int unk21C; int unk220; int unk224; int unk228; int unk22C; int unk230; int unk234; int unk238; int unk23C; int unk240; int unk244; int unk248;
    NiBinaryStream* m_pkIstr;

    void ReadCString(char*& pcString);
    void ReadMultipleLinkIDs(unsigned int uiCount);
    int ReadLinkID();
};

void NiFree(void* p);

template <class T>
inline unsigned int NiBinaryStreamLoad(NiBinaryStream* pkStream, T* pValue, unsigned int uiNumEls)
{
    unsigned int uiSize = sizeof(T);
    return pkStream->BinaryRead(pValue, uiNumEls * sizeof(T), &uiSize, 1);
}

template <class T>
inline unsigned int NiStreamLoadBinary(NiStream& kStream, T& value)
{
    return NiBinaryStreamLoad(kStream.m_pkIstr, &value, 1);
}

inline void LoadBool(NiStream& kStream, bool& bValue)
{
    char cValue = bValue;
    NiStreamLoadBinary(kStream, cValue);
    bValue = (cValue != 0);
}

inline void LoadChar(NiStream& kStream, char& cValue)
{
    NiStreamLoadBinary(kStream, cValue);
}

inline void LoadEnum(NiStream& kStream, int& eValue)
{
    int iValue;
    NiStreamLoadBinary(kStream, iValue);
    eValue = iValue;
}

struct CubeTexBase
{
    virtual void v00();
    virtual void DeleteThis();
    unsigned int m_uiRefCount;
    void IncRefCount() { InterlockedIncrement((long volatile*)&m_uiRefCount); }
    void DecRefCount()
    {
        if (InterlockedDecrement((long volatile*)&m_uiRefCount) == 0)
            DeleteThis();
    }
    void LoadBinaryTexture(NiStream& kStream);
    void LoadBinarySource(NiStream& kStream);
};

struct CubeMapLoader : CubeTexBase
{
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int m_ePixelLayout;
    int m_eAlphaFmt;
    int m_eMipMapped;
    int unk24; int unk28; int unk2C; int unk30; int unk34; int unk38; int unk3C;
    bool m_bStatic;

    void CreateFaces(char* pc0, char* pc1, char* pc2, char* pc3, char* pc4, char* pc5, int iParam);
    void FUN_00a612a0(NiStream& kStream);
};

void CubeMapLoader::FUN_00a612a0(NiStream& kStream)
{
    if (kStream.m_uiNifFileVersion < 0x0A030006)
    {
    LoadBinaryTexture(kStream);
    IncRefCount();

    char cLoad = 0;
    LoadChar(kStream, cLoad);

    char* apcNames[6] = {};
    unsigned int i;
    for (i = 0; i < 6; i++)
        kStream.ReadCString(apcNames[i]);

    kStream.ReadMultipleLinkIDs(6);
    for (i = 0; i < 6; i++)
        kStream.ReadLinkID();

    if (cLoad)
        CreateFaces(apcNames[0], apcNames[1], apcNames[2], apcNames[3], apcNames[4], apcNames[5], kStream.unk1E8);

    for (i = 0; i < 6; i++)
        NiFree(apcNames[i]);

    LoadEnum(kStream, m_ePixelLayout);
    LoadEnum(kStream, m_eMipMapped);
    LoadEnum(kStream, m_eAlphaFmt);
    bool oldStatic = m_bStatic;
    LoadBool(kStream, oldStatic);
    m_bStatic = oldStatic;
    DecRefCount();
    }
    else
    {
        LoadBinarySource(kStream);
    }
}
