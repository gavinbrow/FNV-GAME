// FUN_00c45e00 @ 0x00c45e00 (75 bytes) - __thiscall member, 1 stack parameter (ret 4).
// Add(element) of an NiTArray-style growable array:
//   +0x00 vtable, +0x04 m_pBase, +0x08 m_usMaxSize (u16),
//   +0x0A m_usSize (u16), +0x0C m_usESize (u16), +0x0E m_usGrowBy (u16).
// index = m_usSize; if (index >= m_usMaxSize) grow via FUN_00c45b20
// (m_usGrowBy + index); store element at index via FUN_00c462f0; return index.

struct FUN_00c45e00_class
{
    int unk00;                  // +0x00 vtable pointer (not accessed here)
    int unk04;                  // +0x04 element base pointer (not accessed here)
    unsigned short m_usMaxSize; // +0x08 allocated capacity
    unsigned short m_usSize;    // +0x0A live element count
    unsigned short m_usESize;   // +0x0C (not accessed here)
    unsigned short m_usGrowBy;  // +0x0E grow increment

    void __thiscall FUN_00c45b20(unsigned int uiNewSize);                        // ensure capacity
    void __thiscall FUN_00c462f0(unsigned int uiIndex, unsigned int uiElement);  // store element
    unsigned int __thiscall FUN_00c45e00(unsigned int uiElement);
};

unsigned int FUN_00c45e00_class::FUN_00c45e00(unsigned int uiElement)
{
    struct FUN_00c45e00_pad
    {
        int m00; int m04; int m08; int m0c; int m10; int m14;
        int m18; int m1c; int m20; int m24; int m28; int m2c;
        int m30; int m34; int m38; int m3c; int m40; int m44;
        int m48; int m4c; int m50; int m54; int m58; int m5c;
    };
    FUN_00c45e00_pad kPad;
    {
        unsigned int uiIndex = m_usSize;
        if (uiIndex >= m_usMaxSize)
        {
            FUN_00c45b20(m_usGrowBy + uiIndex);
        }
        FUN_00c462f0(uiIndex, uiElement);
        return uiIndex;
    }
}
