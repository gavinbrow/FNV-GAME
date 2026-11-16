#include "h_54b14390f78f.h"
void NiTArray<BSShaderProperty::RenderPass*, NiTNewInterface<BSShaderProperty::RenderPass*> >::FUN_00ba8d30(unsigned int newSize)
{
    if (newSize != m_usMaxSize) {
        if (newSize < m_usSize) {
            for (unsigned short i = (unsigned short)newSize; i < m_usSize; ++i) {
                if (m_pBase[i] != 0) {
                    m_pBase[i] = 0;
                    m_usESize += 0xffff;
                }
            }
            m_usSize = (unsigned short)newSize;
        }
        BSShaderProperty::RenderPass** oldBase = m_pBase;
        m_usMaxSize = (unsigned short)newSize;
        if (newSize > 0) {
            m_pBase = (BSShaderProperty::RenderPass**)new BSShaderPropertyLightSlot[m_usMaxSize];
            for (unsigned short i = 0; i < m_usSize; ++i)
                m_pBase[i] = oldBase[i];
            for (unsigned short i = m_usSize; i < m_usMaxSize; ++i)
                m_pBase[i] = 0;
        } else {
            m_pBase = 0;
        }
        g_memoryManager.Deallocate(oldBase);
    }
}