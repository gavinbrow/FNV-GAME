struct MessageIconEntry
{
    unsigned char m_storage[16];

    unsigned int FUN_004812d0();
    char* FUN_0047a300();
};

struct BipedModelFormAccess
{
    unsigned char m_precedingComponents[0xa4];
    MessageIconEntry m_messageIcon[2];

    char* FUN_00481280(int sex);
};

// @fnv 0x00481280
char* BipedModelFormAccess::FUN_00481280(int sex)
{
    if (!m_messageIcon[sex].FUN_004812d0() && sex == 1)
    {
        sex = 0;
    }

    return m_messageIcon[sex].FUN_0047a300();
}
