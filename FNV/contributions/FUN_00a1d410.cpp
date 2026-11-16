// Writes every registered compressed entry to "final_master_xml.dat": a 12-byte header, then for each
// entry a 128-byte name, the 4-byte length and the payload. Returns false if any write came up short.
struct CompressedEntry {
    unsigned int m_uiLength;
    unsigned char* m_pucData;
};
extern int DAT_01095574;
extern int DAT_01095524;
extern int DAT_0103d420;
extern int DAT_0103d418;
extern const char DAT_01095548[];
extern const char DAT_01095528[];
void __cdecl FUN_00a02d40(CompressedEntry* apEntry);
void __cdecl FUN_00406d00(char* apBuffer, unsigned int auiSize, const char* apFormat, const char* apName, unsigned int auiLength);
void __cdecl FUN_0040fbe0(const char* apText);
void __cdecl FUN_00aa10f0(void* apMem);
void* __cdecl FUN_00ec61c0(void* apDst, int aiValue, unsigned int auiSize);
int __cdecl FUN_00ec65a6(char* apDst, unsigned int auiSize, const char* apSrc);

struct MapItem { MapItem* m_pkNext; const char* m_pcKey; CompressedEntry* m_pkVal; };
struct EntryMap {
    unsigned int m_uiHashSize;
    unsigned int* m_ppkHashTable;
    unsigned int GetFirstPos()
    {
        for (unsigned int i = 0; i < m_uiHashSize; ++i)
        {
            if (m_ppkHashTable[i])
                return m_ppkHashTable[i];
        }
        return 0;
    }
    virtual void v00();
    virtual unsigned int KeyToHashIndex(const char* pcKey);
    void GetNext(unsigned int& kPos, const char*& pcName, CompressedEntry*& pkEntry)
    {
        MapItem* pkItem = (MapItem*)kPos;
        pcName = pkItem->m_pcKey;
        pkEntry = pkItem->m_pkVal;
        if (pkItem->m_pkNext)
        {
            kPos = (unsigned int)pkItem->m_pkNext;
            return;
        }
        unsigned int i = KeyToHashIndex(pkItem->m_pcKey);
        unsigned int nextBucket = i + 1;
        for (; nextBucket < m_uiHashSize; ++nextBucket)
        {
            pkItem = (MapItem*)m_ppkHashTable[nextBucket];
            if (pkItem)
            {
                kPos = (unsigned int)pkItem;
                return;
            }
        }
        kPos = 0;
    }
};
extern EntryMap DAT_011f34e0;

struct MemoryManager { void* Allocate(unsigned int auiSize); };
extern MemoryManager DAT_011f6238;

struct EntryArray {
    int* m_vtbl;
    CompressedEntry** m_pBase;
    unsigned short m_usMaxSize;
    unsigned short m_usSize;
    unsigned int m_uiGrowBy;
    void FUN_00a1e450(unsigned int auiMax, unsigned int auiGrowBy);
    unsigned int SetAtGrow(unsigned int auiIndex, CompressedEntry*& apEntry);
    CompressedEntry* GetAt(unsigned int i) const { return m_pBase[i]; }
    static void Deallocate(void* apMem) { FUN_00aa10f0(apMem); }
    EntryArray() { FUN_00a1e450(0, 1); m_vtbl = &DAT_01095574; }
    ~EntryArray() { m_vtbl = &DAT_01095524; Deallocate(m_pBase); }
};
struct NameArray {
    int* m_vtbl;
    const char** m_pBase;
    unsigned int m_uiMaxSize;
    unsigned int m_uiSize;
    void FUN_005e0a30(unsigned int auiMax, unsigned int auiGrowBy);
    void Add(const char*& apName);
    const char* GetAt(unsigned int i) const { return m_pBase[i]; }
    static void Deallocate(void* apMem) { FUN_00aa10f0(apMem); }
    NameArray() { FUN_005e0a30(0, 1); m_vtbl = &DAT_0103d420; }
    ~NameArray() { m_vtbl = &DAT_0103d418; Deallocate(m_pBase); }
};

struct BSFileX {
    virtual ~BSFileX();
    unsigned int m_uiAbsoluteCurrentPos;
    int m_iUnk08;
    unsigned int (__cdecl* m_pfnWrite)(BSFileX* apThis, const void* apBuffer, unsigned int auiBytes,
        unsigned int* apuiComponentSizes, unsigned int auiNumComponents);
    unsigned int unk10, unk14, unk18, unk1c, unk20, unk24, unk28, unk2c;
    unsigned int unk30, unk34, unk38, unk3c, unk40, unk44, unk48, unk4c;
    unsigned int unk50, unk54, unk58, unk5c, unk60, unk64, unk68, unk6c;
    unsigned int unk70, unk74, unk78, unk7c, unk80, unk84, unk88, unk8c;
    unsigned int unk90, unk94, unk98, unk9c, unka0, unka4, unka8, unkac;
    unsigned int unkb0, unkb4, unkb8, unkbc, unkc0, unkc4, unkc8, unkcc;
    unsigned int unkd0, unkd4, unkd8, unkdc, unke0, unke4, unke8, unkec;
    unsigned int unkf0, unkf4, unkf8, unkfc, unk100, unk104, unk108, unk10c;
    unsigned int unk110, unk114, unk118, unk11c, unk120, unk124, unk128, unk12c;
    unsigned int unk130, unk134, unk138, unk13c, unk140, unk144, unk148, unk14c;
    unsigned int unk150, unk154;
    BSFileX(const char* apName, int aiMode, unsigned int auiBufferSize, bool abFlag);
    static void* operator new(unsigned int auiSize) { return DAT_011f6238.Allocate(auiSize); }
    static void operator delete(void* apMem);
    unsigned int BinaryWrite(const void* apBuffer, unsigned int auiTotalBytes, unsigned int* apuiComponentSizes,
        unsigned int auiNumComponents)
    {
        unsigned int uiBytesWritten = m_pfnWrite(this, apBuffer, auiTotalBytes, apuiComponentSizes, auiNumComponents);
        m_uiAbsoluteCurrentPos += uiBytesWritten;
        return uiBytesWritten;
    }
    unsigned int Write(const void* apBuffer, unsigned int auiBytes)
    {
        unsigned int uiSize = 1;
        unsigned int uiBytesWritten = BinaryWrite(apBuffer, auiBytes, &uiSize, 1);
        return uiBytesWritten;
    }
};

struct FileHeader {
    unsigned int m_uiVersion;
    unsigned int m_uiCount;
    unsigned int m_uiTotal;
};

bool FUN_00a1d410()
{
    unsigned int a;
    { bool f = true;
    { FileHeader g;
    g.m_uiVersion = 100;
    g.m_uiTotal = 0;
    g.m_uiCount = 0;
    { BSFileX* b;
    { EntryArray records;
    NameArray names;
    unsigned int e = DAT_011f34e0.GetFirstPos();
    while (e != 0)
    {
        char debug[260];
        { CompressedEntry* entry;
        { const char* index;
        DAT_011f34e0.GetNext(e, index, entry);
        FUN_00a02d40(entry);
        records.SetAtGrow(records.m_usSize, entry);
        names.Add(index);
        FUN_00406d00(debug, 0x104, DAT_01095548, index, entry->m_uiLength);
        FUN_0040fbe0(debug);
        g.m_uiTotal += 0x84 + entry->m_uiLength;
        ++g.m_uiCount;
        } }
    }
    b = new BSFileX(DAT_01095528, 1, 0x4000, false);
    a = b->Write(&g, 12);
    if (a == 12)
    {
        for (unsigned int i = 0; i < g.m_uiCount; ++i)
        {
            CompressedEntry* element = records.GetAt(i);
            { char filename[128];
            { const char* name = names.GetAt(i);
            FUN_00ec61c0(filename, 0, 128);
            FUN_00ec65a6(filename, 128, name);
            a = b->Write(filename, 128);
            if (a != 128) f = false;
            a = b->Write(element, 4);
            if (a != 4) f = false;
            a = b->Write(element->m_pucData, element->m_uiLength);
            if (a != element->m_uiLength) f = false;
            if (!f) break;
            } }
        }
    }
    else
    {
        f = false;
    }
    delete b;
    return f;
    }
    }
    }
    }
}