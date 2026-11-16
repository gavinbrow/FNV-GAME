struct NiPSysData_CountView : NiPSysData { unsigned int FUN_00c24ea0(); };
unsigned int NiPSysData_CountView::FUN_00c24ea0() {
    unsigned short count = m_usNumAddedParticles;
    if (count == 0) {
        unsigned short first = m_usActive;
        m_usAddedParticlesBase = first;
        if (first < m_usVertices) {
            return (unsigned short)(first + m_usNumAddedParticles++);
        }
    } else {
        unsigned short base = m_usAddedParticlesBase;
        if (m_usAddedParticlesBase + m_usNumAddedParticles < m_usVertices) {
           return (unsigned short)(base + m_usNumAddedParticles++);
        }
    }
    return 0xffff;
}