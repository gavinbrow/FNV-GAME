struct CC7970_Allocator { void* __thiscall FUN_00aa3e40(unsigned int); };
struct CC7970_RefData { unsigned int m_value; };
struct CC7970_RefObject {
    void* m_pVtable;
    CC7970_RefData m_data;
    unsigned int m_uiRefCount;
    unsigned int m_uiFlags;
    unsigned int m_uiReserved;
};
static __forceinline CC7970_RefData* CC7970_CreateReference() {
    CC7970_RefObject* object = reinterpret_cast<CC7970_RefObject*>(
        reinterpret_cast<CC7970_Allocator*>(&DAT_011f6238)->FUN_00aa3e40(sizeof(CC7970_RefObject)));
    if (object) {
        CC7970_RefData* data = &object->m_data;
        object->m_uiRefCount = 1;
        object->m_uiFlags = 0;
        object->m_uiReserved = 0;
        object->m_pVtable = &DAT_010c9d60;
        data->m_value = 0;
        return data;
    }
    return 0;
}
struct CC7970_Owner {
    unsigned int m_unk00, m_unk04, m_flag08;
    CC7970_RefData* m_pData;
    void __thiscall FUN_00c89c80(CC7970_RefObject* object);
    CC7970_RefData* __thiscall FUN_00cc7970(bool* created);
};
CC7970_RefData* CC7970_Owner::FUN_00cc7970(bool* created) {
    TlsFlagGuard tlsGuard;
    *created = (m_pData == 0);
    if (*created) {
        CC7970_RefData* data = CC7970_CreateReference();
        m_pData = data;
        if (m_flag08) {
            FUN_00c89c80(data ? reinterpret_cast<CC7970_RefObject*>(reinterpret_cast<char*>(data) - 4) : 0);
        }
    }
    return m_pData;
}