struct hkMemoryAllocStub {
    virtual void unk00();
    virtual void unk04();
    virtual void unk08();
    virtual void unk0C();
    virtual void deallocateChunk(void* p, int nbytes);
};

template <class T>
struct hkArrayRaw {
    T* m_data;
    int m_size;
    int m_capacityAndFlags;

};

template <class T>
struct hkArrayStub {
    T* m_data;
    int m_size;
    int m_capacityAndFlags;

    hkArrayStub() : m_data(0), m_size(0), m_capacityAndFlags(0x80000000) {}
    ~hkArrayStub()
    {
        hkMemoryAllocStub* mem = reinterpret_cast<hkMemoryAllocStub*>(FUN_00c85750()->unk10);
        if ((m_capacityAndFlags & 0x80000000) == 0)
            mem->deallocateChunk(m_data, (m_capacityAndFlags & 0x3fffffff) * sizeof(T));
    }
    hkArrayStub(const hkArrayRaw<T>& r) : m_data(r.m_data), m_size(r.m_size), m_capacityAndFlags(r.m_capacityAndFlags) {}
    __forceinline hkArrayRaw<T> release()
    {
        int s = m_size;
        T* d = m_data;
        m_data = 0;
        m_size = 0;
        int c = m_capacityAndFlags;
        m_capacityAndFlags = 0x80000000;
        hkArrayRaw<T> r;
        r.m_data = d;
        r.m_size = s;
        r.m_capacityAndFlags = c;
        return r;
    }
    void swap(hkArrayStub& a)
    {
        int s = a.m_size;
        T* d = a.m_data;
        a.m_data = m_data;
        a.m_size = m_size;
        m_data = d;
        m_size = s;
        int c = a.m_capacityAndFlags;
        a.m_capacityAndFlags = m_capacityAndFlags;
        m_capacityAndFlags = c;
    }
};

struct NiBinaryStreamStub {
    void* m_pVtable;
    unsigned int m_uiAbsoluteCurrentPos;
    void* m_pfnRead;
    unsigned int (*m_pfnWrite)(NiBinaryStreamStub* stream, const void* buffer, unsigned int bytes,
                               unsigned int* componentSizes, unsigned int numComponents);

    void BinaryWrite(const void* buffer, unsigned int bytes, unsigned int* componentSizes, unsigned int numComponents)
    {
        m_uiAbsoluteCurrentPos += m_pfnWrite(this, buffer, bytes, componentSizes, numComponents);
    }
};

template <class T>
inline void SaveBinaryValue(NiBinaryStreamStub* stream, const T& value)
{
    unsigned int uiSize = sizeof(T);
    stream->BinaryWrite(&value, sizeof(T), &uiSize, 1);
}

struct LinkedObjStub {
    int unk00;
    int unk04;
    void* m_pLinked;
};

struct SaveStreamStub {
    virtual void v00(); virtual void v04(); virtual void v08(); virtual void v0C();
    virtual void v10(); virtual void v14(); virtual void v18(); virtual void v1C();
    virtual void v20(); virtual void v24(); virtual void v28(); virtual void v2C();
    virtual void SaveLinkID(void* obj);
};

struct SaveStreamFields : SaveStreamStub {
    int unk004; int unk008; int unk00C; int unk010; int unk014; int unk018; int unk01C;
    int unk020; int unk024; int unk028; int unk02C; int unk030; int unk034; int unk038; int unk03C;
    int unk040; int unk044; int unk048; int unk04C; int unk050; int unk054; int unk058; int unk05C;
    int unk060; int unk064; int unk068; int unk06C; int unk070; int unk074; int unk078; int unk07C;
    int unk080; int unk084; int unk088; int unk08C; int unk090; int unk094; int unk098; int unk09C;
    int unk0A0; int unk0A4; int unk0A8; int unk0AC; int unk0B0; int unk0B4; int unk0B8; int unk0BC;
    int unk0C0; int unk0C4; int unk0C8; int unk0CC; int unk0D0; int unk0D4; int unk0D8; int unk0DC;
    int unk0E0; int unk0E4; int unk0E8; int unk0EC; int unk0F0; int unk0F4; int unk0F8; int unk0FC;
    int unk100; int unk104; int unk108; int unk10C; int unk110; int unk114; int unk118; int unk11C;
    int unk120; int unk124; int unk128; int unk12C; int unk130; int unk134; int unk138; int unk13C;
    int unk140; int unk144; int unk148; int unk14C; int unk150; int unk154; int unk158; int unk15C;
    int unk160; int unk164; int unk168; int unk16C; int unk170; int unk174; int unk178; int unk17C;
    int unk180; int unk184; int unk188; int unk18C; int unk190; int unk194; int unk198; int unk19C;
    int unk1A0; int unk1A4; int unk1A8; int unk1AC; int unk1B0; int unk1B4; int unk1B8; int unk1BC;
    int unk1C0; int unk1C4; int unk1C8; int unk1CC; int unk1D0; int unk1D4; int unk1D8; int unk1DC;
    int unk1E0;
    unsigned char m_bUnk1E4;
    unsigned char unk1E5; unsigned short unk1E6;
    int unk1E8; int unk1EC;
    int unk1F0; int unk1F4; int unk1F8; int unk1FC;
    int unk200; int unk204; int unk208; int unk20C; int unk210; int unk214; int unk218; int unk21C;
    int unk220; int unk224; int unk228; int unk22C; int unk230; int unk234; int unk238; int unk23C;
    int unk240; int unk244; int unk248; int unk24C;
    NiBinaryStreamStub* m_pOstr;
};

struct CountedSub {
    virtual void v00();
    virtual int GetCount();
};

struct CountedOwner {
    int unk00; int unk04; int unk08; int unk0C; int unk10;
    CountedSub m_sub;
};

struct SavedData {
    int unk00;
    int unk04;
    char m_cUnk08;
    int m_iUnk0C;
    hkArrayStub<LinkedObjStub*> m_array;
};

void FUN_00cf0930(SavedData* data, void* source, hkArrayStub<LinkedObjStub*>* out);

struct bhkSaveOwner {
    virtual void v00(); virtual void v04(); virtual void v08(); virtual void v0C();
    virtual void v10(); virtual void v14(); virtual void v18(); virtual void v1C();
    virtual void v20(); virtual void v24(); virtual void v28(); virtual void v2C();
    virtual void v30(); virtual void v34(); virtual void v38(); virtual void v3C();
    virtual void v40(); virtual void v44(); virtual void v48(); virtual void v4C();
    virtual void v50(); virtual void v54(); virtual void v58(); virtual void v5C();
    virtual void v60(); virtual void v64(); virtual void v68(); virtual void v6C();
    virtual void v70(); virtual void v74(); virtual void v78(); virtual void v7C();
    virtual void v80(); virtual void v84(); virtual void v88(); virtual void v8C();
    virtual void v90(); virtual void v94(); virtual void v98(); virtual void v9C();
    virtual void vA0(); virtual void vA4();
    virtual void* GetSource();
    virtual void vAC(); virtual void vB0();
    virtual SavedData* GetData(bool* pbOut);

    int unk04;
    CountedOwner* m_pOwner;

    int GetCount() { CountedOwner* owner = m_pOwner; return owner ? owner->m_sub.GetCount() : 0; }
    void FUN_00c9fc00(SaveStreamFields* stream);
    void FUN_00cd02d0(SaveStreamFields* stream);
};

void bhkSaveOwner::FUN_00cd02d0(SaveStreamFields* stream)
{
    bool bOut;
    SavedData* data = GetData(&bOut);
    hkArrayStub<LinkedObjStub*> arr;
    arr.swap(data->m_array);
    if (stream->m_bUnk1E4 != 1) {
        void* source = GetSource();
        FUN_00cf0930(data, source, &data->m_array);
    }
    int count = arr.m_size;
    SaveBinaryValue(stream->m_pOstr, count);
    for (int i = 0; i < GetCount(); i++) {
        LinkedObjStub* obj = arr.m_data[i];
        stream->SaveLinkID(obj ? obj->m_pLinked : 0);
    }
    FUN_00c9fc00(stream);
    SaveBinaryValue(stream->m_pOstr, data->m_cUnk08);
    SaveBinaryValue(stream->m_pOstr, data->m_iUnk0C);
}
