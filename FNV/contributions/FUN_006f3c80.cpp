struct FUN_00982610 {
    unsigned int m_root;
    unsigned int m_capacity;
    unsigned int m_count;
    unsigned int m_allocated;
    ~FUN_00982610();
};

struct FUN_00483710 {
    unsigned int m_root;
    unsigned int m_capacity;
    unsigned int m_count;
    unsigned int m_allocated;
    ~FUN_00483710();
};

struct EntryTable : FUN_00483710 {
    unsigned int m_entries[2036];
};

struct FUN_006f3c80 {
    FUN_00982610 m_heap;
    EntryTable m_entries;
    FUN_00483710 m_lookup;
    unsigned int m_count;
    unsigned int m_capacity;
    unsigned int m_index;
    unsigned char m_initialized;
    virtual ~FUN_006f3c80();
};

FUN_006f3c80::~FUN_006f3c80()
{
}
