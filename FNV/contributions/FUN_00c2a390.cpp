extern float DAT_010c09c0;

struct ParticleInfo_00c2a390 {
    float unk00;
    float unk04;
    float unk08;
    float age;
    float lifeSpan;
    unsigned int unk14;
    unsigned short generation;
    unsigned short unk1a;
};
struct ParticleData_00c2a390 {
    unsigned int unk00, unk04, unk08, unk0c;
    unsigned int unk10, unk14, unk18, unk1c;
    unsigned int unk20, unk24, unk28, unk2c;
    unsigned int unk30, unk34, unk38, unk3c;
    unsigned int unk40, unk44, unk48, unk4c;
    unsigned short activeCount;
    unsigned short maxCount;
    float* scales;
    unsigned int unk58, unk5c, unk60, unk64, unk68, unk6c;
    ParticleInfo_00c2a390* particles;
};
struct FUN_00c2a390_shell : NiPSysGrowFadeModifier {
    void FUN_00c2a390(unsigned int, ParticleData_00c2a390*);
};

void FUN_00c2a390_shell::FUN_00c2a390(unsigned int, ParticleData_00c2a390* data) {
    float scaleRange = 1.0f - m_fBaseScale;
    for (unsigned short i = 0; i < data->activeCount; ++i) {
        const ParticleInfo_00c2a390& particle = data->particles[i];
        float fade = 1.0f;
        if (particle.generation == m_usGrowGeneration &&
            particle.age < m_fGrowTime && m_fGrowTime != 0.0f) {
            fade = particle.age / m_fGrowTime;
        }

        float grow = 1.0f;
        float remaining = particle.lifeSpan - particle.age;
        if (particle.generation == m_usFadeGeneration &&
            remaining < m_fFadeTime && m_fFadeTime != 0.0f) {
            grow = remaining / m_fFadeTime;
        }
        float ratio = grow > fade ? fade : grow;
        float scale = ratio * scaleRange + m_fBaseScale;
        if (scale < DAT_010c09c0) {
            scale = DAT_010c09c0;
        }
        data->scales[i] = scale;
    }
}