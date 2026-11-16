struct FUN_00a84ca0_entry {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    void* unk44;
    int unk48;
};

struct MemoryManager {
    void Deallocate(void*);
};

extern MemoryManager g_memoryManager;

struct FUN_00a84ca0_class {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    void* m_40;
    unsigned int m_44;

    void FUN_00a84ca0();
};

void FUN_00a84ca0_class::FUN_00a84ca0()
{
    if (m_40 != 0) {
        for (unsigned int i = 0; i < m_44; ++i) {
            g_memoryManager.Deallocate(
                reinterpret_cast<FUN_00a84ca0_entry*>(m_40)[i].unk44);
            reinterpret_cast<FUN_00a84ca0_entry*>(m_40)[i].unk44 = 0;
        }
    }
}