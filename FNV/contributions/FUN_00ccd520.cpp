
extern "C" __declspec(thread) int g_currentMemoryContext;
extern "C" float DAT_010c72bc;

struct MemoryHeap {
    void* __thiscall FUN_00aa3e40(unsigned int byteCount);
};
extern MemoryHeap DAT_011f6238;

struct TransformRecord {
    unsigned int m_flags;
    float m_scalar;
    unsigned int m_unk08;
    unsigned int m_unk0c;
    float m_translationX;
    float m_translationY;
    float m_translationZ;
    float m_translationW;
    volatile float m_rotationW;
    volatile float m_rotationX;
    volatile float m_rotationY;
    volatile float m_rotationZ;
    float m_other;
};

struct MemoryContextScope {
    int previousContext;
    MemoryContextScope() {
        previousContext = g_currentMemoryContext;
        g_currentMemoryContext = 0x10;
    }
    ~MemoryContextScope() {
        g_currentMemoryContext = previousContext;
    }
};

struct TransformHolder {
    void* m_vtable;
    unsigned int m_refCount;
    int m_enableCallback;
    TransformRecord* m_record;
    void __thiscall FUN_00ccd1d0(TransformRecord* transform);
    TransformRecord* __thiscall FUN_00ccd520(bool* created);
};

TransformRecord* TransformHolder::FUN_00ccd520(bool* created) {
    MemoryContextScope memoryContext;
    bool isNew = m_record == 0;
    *created = isNew;
    if (isNew) {
        char* allocation = (char*)DAT_011f6238.FUN_00aa3e40(0x50); unsigned char delta=(unsigned char)(16 - (unsigned char)((unsigned int)allocation & 0xf)); allocation[delta - 1] = delta; allocation += delta; TransformRecord* record=(TransformRecord*)allocation;
        record->m_flags = 0;
        record->m_scalar = DAT_010c72bc;
        record->m_translationX = 0.0f;
        record->m_translationY = 0.0f;
        record->m_translationZ = 0.0f;
        record->m_translationW = 0.0f;
        record->m_rotationW = 0.0f;
        record->m_rotationX = 0.0f;
        record->m_rotationY = 0.0f;
        record->m_rotationZ = 0.0f;
        record->m_other = 0.0f;
        record->m_rotationW = 1.0f;
        record->m_rotationX = 0.0f;
        record->m_rotationY = 0.0f;
        record->m_rotationZ = 0.0f;
        m_record = record;
        if (m_enableCallback) {
            FUN_00ccd1d0(record);
        }
    }
    return m_record;
}
