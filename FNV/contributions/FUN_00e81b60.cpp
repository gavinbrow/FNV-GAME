struct FUN_00e81b60_Entry {
    unsigned int m_key;
    int m_value;
};

struct FUN_00e81b60_Class {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int m_index[3];
    FUN_00e81b60_Entry* m_entries[3];

    int __thiscall FUN_00e81b60(unsigned int a, unsigned int b, int c, int d);
};

extern int DAT_01101294;

int FUN_00e81b60_Class::FUN_00e81b60(unsigned int a, unsigned int b, int c, int d)
{
    unsigned int key = (b << DAT_01101294) | a;
    unsigned int index = m_index[c];

    if (m_entries[c][index].m_key == key) {
        int result = m_entries[c][index].m_value;
        m_index[c] = index + 1;
        return result;
    }

    return 0;
}