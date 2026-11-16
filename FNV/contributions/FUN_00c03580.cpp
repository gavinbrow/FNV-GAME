
struct DestroyableReference {
    virtual ~DestroyableReference();
};

struct Handle {
    void FUN_00ba3a00();
};

struct HandlePool {
    void FUN_00aa4060(Handle* handle);
};
extern HandlePool DAT_011f6238;

struct RefMapEntries {
    int m_zero;
    DestroyableReference* m_first;
    int m_eight;
    DestroyableReference* m_third;
};

struct HandleMapEntries {
    int m_zero;
    int m_four;
    Handle* m_second;
    Handle* m_third;
};

struct ElementMap {
    int m_unknown;
    void* m_entries;
    int m_count;
    int m_capacity;
    void FUN_00ba3aa0(unsigned int index, int* newValue);
};

struct Entry {
    int m_zero;
    int m_four;
    int m_eight;
    int m_twelve;
    ~Entry();
};

struct Parent {
    virtual ~Parent();
};

struct FUN_00c03580 : Parent {
    int m_04;
    int m_08;
    int m_0c;
    int m_10;
    int m_14;
    ElementMap m_refs;
    ElementMap m_handles;
    int m_38;
    int m_3c;
    int m_40;
    int m_44;
    int m_48;
    int m_4c;
    int m_50;
    int m_54;
    int m_58;
    Entry m_entries[2];

    ~FUN_00c03580();
};

FUN_00c03580::~FUN_00c03580()
{
    if (static_cast<HandleMapEntries*>(m_handles.m_entries)->m_second) {
        Handle* handle = static_cast<HandleMapEntries*>(m_handles.m_entries)->m_second;
        if (handle) {
            handle->FUN_00ba3a00();
            DAT_011f6238.FUN_00aa4060(handle);
        }
        int cleared = 0;
        m_handles.FUN_00ba3aa0(2, &cleared);
    }

    if (static_cast<HandleMapEntries*>(m_handles.m_entries)->m_third) {
        Handle* handle = static_cast<HandleMapEntries*>(m_handles.m_entries)->m_third;
        if (handle) {
            handle->FUN_00ba3a00();
            DAT_011f6238.FUN_00aa4060(handle);
        }
        int cleared = 0;
        m_handles.FUN_00ba3aa0(3, &cleared);
    }

    if (static_cast<RefMapEntries*>(m_refs.m_entries)->m_first) {
        DestroyableReference* ref = static_cast<RefMapEntries*>(m_refs.m_entries)->m_first;
        if (ref) {
            delete ref;
        }
        int cleared = 0;
        m_refs.FUN_00ba3aa0(1, &cleared);
    }

    if (static_cast<RefMapEntries*>(m_refs.m_entries)->m_third) {
        DestroyableReference* ref = static_cast<RefMapEntries*>(m_refs.m_entries)->m_third;
        if (ref) {
            delete ref;
        }
        int cleared = 0;
        m_refs.FUN_00ba3aa0(3, &cleared);
    }
}
