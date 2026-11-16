struct FUN_0084d310_entry;

struct FUN_0084d310_class {
    virtual void FUN_0084d310_slot0() = 0;
    virtual int FUN_0084d310_lookup(int key) = 0;
    virtual bool FUN_0084d310_match(int key, int value) = 0;
    virtual void FUN_0084d310_create(void* node, int key, unsigned char value) = 0;
    virtual void FUN_0084d310_unused() = 0;
    virtual void* FUN_0084d310_allocate() = 0;

    void* unk04;
    FUN_0084d310_entry** m_buckets;
    unsigned int m_count;

    void FUN_0084d310(int key, unsigned char value);
};

struct FUN_0084d310_entry {
    FUN_0084d310_entry* m_next;
    int m_key;
    unsigned char m_value;
};

void FUN_0084d310_class::FUN_0084d310(int key, unsigned char value)
{
    int index = FUN_0084d310_lookup(key);
    FUN_0084d310_entry* entry = m_buckets[index];
    int count = 0;

    while (entry != 0) {
        ++count;
        if (FUN_0084d310_match(key, entry->m_key)) {
            entry->m_value = value;
            return;
        }
        entry = entry->m_next;
    }

    entry = static_cast<FUN_0084d310_entry*>(FUN_0084d310_allocate());

    FUN_0084d310_create(entry, key, value);
    entry->m_next = m_buckets[index];
    m_buckets[index] = entry;
    ++m_count;
}