#include "h_74712c1d3c73.h"

struct H2 {
    virtual void v0();
    virtual void* v1(unsigned int count);
    void* m_data;
    unsigned int m_size;
    unsigned int m_capacity;
    void FUN_006a8890(unsigned int newSize, unsigned char doShrink);
    void FUN_008454f0(unsigned char doShrink);
    void FUN_006dc590(unsigned int newCapacity, unsigned int currentSize);
    void FUN_006d03d0(void* first, unsigned int count);
    void FUN_0072ba80(void* first, unsigned int count);
};

void H2::FUN_006a8890(unsigned int newSize, unsigned char doShrink)
{
    if (newSize == 0)
    {
        FUN_008454f0(doShrink);
    }
    else if (newSize > m_capacity)
    {
        if (m_capacity == 0)
        {
            m_data = v1(newSize);
            m_capacity = newSize;
        }
        else
        {
            FUN_006dc590(newSize, m_size);
            m_capacity = newSize;
        }
        FUN_006d03d0((char*)m_data + m_size * 12, newSize - m_size);
        m_size = newSize;
    }
    else if (newSize < m_size)
    {
        FUN_0072ba80((char*)m_data + newSize * 12, m_size - newSize);
        m_size = newSize;
        if (doShrink && newSize <= (m_capacity >> 2))
        {
            FUN_006dc590(newSize, newSize);
            m_capacity = newSize;
        }
    }
    else
    {
        FUN_006d03d0((char*)m_data + m_size * 12, newSize - m_size);
        m_size = newSize;
    }
}

