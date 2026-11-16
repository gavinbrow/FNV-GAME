struct ParticleViewFrame {
    unsigned int unk_00;
    unsigned int unk_04;
    unsigned int unk_08;
    unsigned int unk_0c;
    unsigned int unk_10;
    unsigned int unk_14;
    unsigned int unk_18;
    unsigned int unk_1c;
    unsigned int unk_20;
    unsigned int unk_24;
    unsigned int unk_28;
    unsigned int unk_2c;
    unsigned int unk_30;
    unsigned int unk_34;
    unsigned int unk_38;
    unsigned int unk_3c;
    unsigned int unk_40;
    unsigned int unk_44;
    unsigned int unk_48;
    unsigned int unk_4c;
    unsigned int unk_50;
    unsigned int unk_54;
    unsigned int unk_58;
    unsigned int unk_5c;
    unsigned int unk_60;
    NiPoint3 axisX, axisY, axisZ;
};
extern MemoryManager g_memoryManager;
inline void* operator new[](unsigned int bytes, MemoryManager& manager) { return manager.Allocate(bytes); }
struct SortParticles : NiParticlesData { void FUN_00a966c0(int,int); void FUN_00a96910(ParticleViewFrame*); };
void SortParticles::FUN_00a96910(ParticleViewFrame* view) {
if (!m_ausRenderOrder) { m_ausRenderOrder = new (g_memoryManager) unsigned short[m_usVertices]; m_afDepths = new (g_memoryManager) float[m_usVertices]; }
for (unsigned short i = 0; i < m_usActive; ++i) m_ausRenderOrder[i] = i;
if (m_usActive > 1) {
NiPoint3 direction = {view->axisX.y, view->axisY.y, view->axisZ.y};
for (unsigned short i = 0; i < m_usActive; ++i) {
const NiPoint3& p = m_pkVertex[i];
m_afDepths[i] = p.Dot(direction);
} FUN_00a966c0(0, m_usActive - 1);
} }