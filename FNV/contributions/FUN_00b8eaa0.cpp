extern char DAT_010b1c90;
extern char DAT_010b1c70;
void __cdecl FUN_00c03a20();
void __cdecl FUN_00aa1460(void* object, unsigned int size);

struct FNVObjectToDispose {
    void* m_primaryVtable;
    unsigned int m_unknown04;
    unsigned int m_unknown08;
    unsigned int m_unknown0c;
    unsigned int m_unknown10;
    unsigned int m_unknown14;
    unsigned int m_unknown18;
    unsigned int m_unknown1c;
    unsigned int m_unknown20;
    unsigned int m_unknown24;
    unsigned int m_unknown28;
    unsigned int m_unknown2c;
    unsigned int m_unknown30;
    unsigned int m_unknown34;
    unsigned int m_unknown38;
    unsigned int m_unknown3c;
    unsigned int m_unknown40;
    unsigned int m_unknown44;
    unsigned int m_unknown48;
    unsigned int m_unknown4c;
    unsigned int m_unknown50;
    unsigned int m_unknown54;
    unsigned int m_unknown58;
    unsigned int m_unknown5c;
    unsigned int m_unknown60;
    unsigned int m_unknown64;
    unsigned int m_unknown68;
    void* m_secondaryVtable;
    FNVObjectToDispose* FUN_00b8eaa0(unsigned char flags);
};

FNVObjectToDispose* FNVObjectToDispose::FUN_00b8eaa0(unsigned char flags) {
    m_primaryVtable = &DAT_010b1c90;
    m_secondaryVtable = &DAT_010b1c70;
    FUN_00c03a20();
    if (flags & 1)
        FUN_00aa1460(this, 208);
    return this;
}
