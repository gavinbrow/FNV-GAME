extern char DAT_0105c390;
extern char DAT_010cb2d8;
extern char DAT_01020e44;
extern char DAT_010cb2c8;
void* __cdecl FUN_00d06f80(void* data, int bytes);

struct hkStreamWriter {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void WriteField(const void* field, const void* data, int flags);
    virtual void v10();
    virtual void WriteArray(int kind, const void* field, const void* data, int bytes, void* allocation);

    int unk04;
    int unk08;
    int unk0C;
    unsigned char m_includeOwned;

    void FUN_00d06fb0(const void* field, const void* data, int bytes, int flags);
};

struct FNVWorldObject : hkpWorldObject {
    void FUN_00cd2b00(hkStreamWriter* writer, int unused);
};

void FNVWorldObject::FUN_00cd2b00(hkStreamWriter* writer, int unused)
{
    writer->WriteField(&DAT_0105c390, m_collidable.m_shape, 0);

    hkArray<char>& entries = m_collidable.m_collisionEntries;
    int entryCap = entries.m_capacityAndFlags;
    if ((entryCap & 0x80000000) == 0 || writer->m_includeOwned) {
        void* entryData = entries.m_data;
        void* copy = FUN_00d06f80(entryData, (entryCap & 0x3fffffff) * 8);
        writer->WriteArray(3, &DAT_010cb2d8, entries.m_data, entries.m_size * 8, copy);
    }

    int propCap = m_properties.m_capacityAndFlags;
    if ((propCap & 0x80000000) == 0 || writer->m_includeOwned) {
        void* propData = m_properties.m_data;
        void* copy = FUN_00d06f80(propData, (propCap & 0x3fffffff) * 16);
        writer->WriteArray(3, &DAT_01020e44, m_properties.m_data, m_properties.m_size * 16, copy);
    }

    hkpCollidableBoundingVolumeData& bounds = m_collidable.m_boundingVolumeData;
    void* firstChild = bounds.m_childShapeAabbs;
    if (firstChild) {
        writer->FUN_00d06fb0(&DAT_010cb2c8, firstChild, (unsigned int)bounds.m_capacityChildShapeAabbs * 32, 0);
        writer->FUN_00d06fb0(&DAT_010cb2c8, bounds.m_childShapeKeys, (unsigned int)bounds.m_capacityChildShapeAabbs * 4, 0);
    }
}
