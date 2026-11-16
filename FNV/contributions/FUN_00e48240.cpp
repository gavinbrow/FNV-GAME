extern int DAT_010e81a4;

struct FUN_00e48240 {
    void* m_vTable;
    short m_flags;
    short m_initialized;
    int m_value;
    FUN_00e48240(int value);
};

FUN_00e48240::FUN_00e48240(int value)
{
    m_initialized = 1;
    m_vTable = &DAT_010e81a4;
    m_value = value;
}