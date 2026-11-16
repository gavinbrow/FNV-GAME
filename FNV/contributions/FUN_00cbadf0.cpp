class CBADDynamicArray : public CA0E60Array {
public:
    void FUN_00cb9d50(void** elements, unsigned int count);
    void FUN_00cba0d0(void** elements, unsigned int count);
    void FUN_00cbadf0(unsigned int requestedSize, bool compact);
};

void CBADDynamicArray::FUN_00cbadf0(unsigned int requestedSize, bool compact)
{
    if (requestedSize == 0) {
        if (m_pBuffer != 0) {
            FUN_00cba0d0(m_pBuffer, m_uiSize);
            if (compact) {
                Free(m_pBuffer);
                m_pBuffer = 0;
                m_uiAllocSize = 0;
            }
            m_uiSize = 0;
        }
        return;
    }

    if (requestedSize > m_uiAllocSize) {
        if (m_uiAllocSize == 0) {
            m_pBuffer = Allocate(requestedSize);
        } else {
            FUN_00cb9ce0(requestedSize, m_uiSize);
        }
        unsigned int oldSize = m_uiSize;
        m_uiAllocSize = requestedSize;
        FUN_00cb9d50(m_pBuffer + oldSize, requestedSize - oldSize);
        m_uiSize = requestedSize;
    } else if (requestedSize < m_uiSize) {
        FUN_00cba0d0(m_pBuffer + requestedSize, m_uiSize - requestedSize);
        m_uiSize = requestedSize;
        if (compact && requestedSize <= m_uiAllocSize / 4) {
            FUN_00cb9ce0(requestedSize, requestedSize);
            m_uiAllocSize = requestedSize;
        }
    } else {
        unsigned int oldSize = m_uiSize;
        FUN_00cb9d50(m_pBuffer + oldSize, requestedSize - oldSize);
        m_uiSize = requestedSize;
    }
}
