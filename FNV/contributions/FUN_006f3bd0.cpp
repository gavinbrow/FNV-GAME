
extern unsigned int DAT_0106d90c;

struct FUN_006f4320 {
    unsigned int m_root;
    unsigned int m_capacity;
    unsigned int m_count;
    unsigned int m_allocated;
    FUN_006f4320();
    ~FUN_006f4320();
};

struct FUN_006b3de0 {
    unsigned int m_entries[2040];
    FUN_006b3de0();
    ~FUN_006b3de0();
};

struct FUN_006b9470 {
    unsigned int m_words[21];
    FUN_006b9470();
};

struct FUN_006f3bd0 {
    unsigned int* m_vtable;
    FUN_006f4320 m_heap;
    FUN_006b3de0 m_entries;
    FUN_006b9470 m_lookup;
    unsigned int m_count;
    unsigned int m_capacity;
    unsigned int m_index;
    unsigned char m_initialized;
    FUN_006f3bd0();
};

FUN_006f3bd0::FUN_006f3bd0()
    : m_vtable(&DAT_0106d90c),
      m_count(0),
      m_capacity(0),
      m_index(0),
      m_initialized(0) {
}
