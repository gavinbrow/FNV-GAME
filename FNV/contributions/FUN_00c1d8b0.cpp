extern int _DAT_012024fc;
extern int _DAT_012024f8;
extern char UNK_00fdd3b0;
void __cdecl FUN_00ec658f(void*);

struct FUN_00c1d8b0_class {
    void** m_vtable;
    RefObject** m_pBase;
    unsigned short m_usMaxSize;
    unsigned short m_usSize;
    unsigned short m_usESize;
    unsigned short m_usGrowBy;
    void FUN_00c1d8b0(unsigned int index, RefObject** value);
};

void FUN_00c1d8b0_class::FUN_00c1d8b0(unsigned int index, RefObject** value)
{
    int one = 1;
    if ((*(unsigned char*)&_DAT_012024fc & one) == 0) {
        _DAT_012024fc |= one;
        _DAT_012024f8 = 0;
        FUN_00ec658f(&UNK_00fdd3b0);
    }

    if (index >= m_usSize) {
        m_usSize = (unsigned short)(index + 1);
        if (*value != (RefObject*)_DAT_012024f8)
            m_usESize += one;
    } else {
        if (*value != (RefObject*)_DAT_012024f8) {
            if (m_pBase[index] == (RefObject*)_DAT_012024f8)
                m_usESize += one;
        } else if (m_pBase[index] != (RefObject*)_DAT_012024f8) {
            m_usESize += 0xffff;
        }
    }

    RefObject** slot = &m_pBase[index];
    RefObject* oldValue = *slot;
    if (oldValue != *value) {
        if (oldValue != 0) {
            if (DAT_00fdf1c4(&oldValue->m_refCount) == 0)
                oldValue->DeleteThis();
        }
        RefObject* newValue = *value;
        *slot = newValue;
        if (newValue != 0)
            DAT_00fdf1c0(&newValue->m_refCount);
    }
}