struct hkBoolQ {
    hkBoolQ(int b) { m_bool = (char)b; }
    operator bool() const { return m_bool != 0; }
    char m_bool;
};

template <class T> struct hkArrayQ {
    T* m_data;
    int m_size;
    int m_capacityAndFlags;
    int getSize() const { return m_size; }
    T& operator[](int i) { return m_data[i]; }
};

class hkpSimulationIslandQ {
public:
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    unsigned char unk24;
    unsigned char m_splitCheckRequested : 2;
    unsigned char m_sparseEnabled : 2;
    unsigned char m_flags25hi : 4;
    unsigned char m_flags26lo : 2;
    unsigned char m_activeMark : 2;
    unsigned char m_flags26hi : 4;
    unsigned char unk27;
    int unk28;
    int unk2C;
    int unk30;
    int unk34;
    int unk38;
    int unk3C;
    int unk40;
    int unk44;
    hkArrayQ<hkpEntity*> m_entities;

    hkBoolQ isActive() const { return m_activeMark; }
};


extern float DAT_0104da48;
void __cdecl FUN_00cb6e70(FUN_00c9c3c0_Class* world, hkpSimulationIslandQ* island);
void __cdecl FUN_00cb5420(FUN_00c9c3c0_Class* world, hkpSimulationIslandQ* island);
void FUN_00c9c240_holder::FUN_00c9c240()
{
    hkpSimulationIslandQ* island = (hkpSimulationIslandQ*)m_simulationIsland;
    if (island)
    {
        unsigned char act = island->m_activeMark;
        unsigned char* pact = &act;
        if (*pact)
        {
            if (island->m_splitCheckRequested || island->m_sparseEnabled)
            {
                FUN_00c9c3c0_Class* world = (FUN_00c9c3c0_Class*)m_world;
                int minIslandSize = world->m_b4;
                world->m_b4 = 0;
                ((hkpSimulationIslandQ*)m_simulationIsland)->m_sparseEnabled = 0;
                ((hkpSimulationIslandQ*)m_simulationIsland)->m_splitCheckRequested = 1;
                FUN_00cb6e70((FUN_00c9c3c0_Class*)m_world, (hkpSimulationIslandQ*)m_simulationIsland);
                ((FUN_00c9c3c0_Class*)m_world)->m_b4 = minIslandSize;
            }
            island = (hkpSimulationIslandQ*)m_simulationIsland;
            int i = 0;
            if (island->m_entities.getSize() > 0)
            {
                hkpEntity** entities = island->m_entities.m_data;
                do
                {
                    hkpEntity* entity = *entities++;
                    entity->m_motion.m_deactivationRefPosition[0].w = 3.40282e+38f;
                    entity->m_motion.m_deactivationRefPosition[1].w = 3.40282e+38f;
                } while (++i < island->m_entities.getSize());
            }
            FUN_00cb5420((FUN_00c9c3c0_Class*)m_world, island);
        }
    }
}
