
struct ListenerCollection {
    void* unk00; void* unk04; void* unk08; void* unk0C;
    void* unk10; void* unk14; void* unk18; void* unk1C;
    void* unk20; void* unk24; void* unk28; void* unk2C;
    void* unk30; void* unk34; void* unk38; void* unk3C;
    void* unk40; void* unk44; void* unk48; void* unk4C;
    void* unk50; void* unk54; void* unk58; void* unk5C;
    void* unk60; void* unk64; void* unk68;
    void** m_items;
    int m_count;
};
struct FUN_00d66330_StandIn {
    void* m_vtable;
    void* unk04;
    void* unk08;
    void* unk0C;
    void* unk10;
    void* unk14;
    void* unk18;
    ListenerCollection* m_collection;
    void FUN_00d66330();
};
void FUN_00d66330_StandIn::FUN_00d66330() {
    if (m_collection) {
        for (int i = 0; i < m_collection->m_count; ++i) {
            reinterpret_cast<FUN_00d662c0_stub*>(
                reinterpret_cast<char*>(this) - 8)->FUN_00d662c0(m_collection->m_items[i]);
        }
    }
}
