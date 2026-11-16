struct FNVArray {
    int* m_data;
    int m_size;
    unsigned int m_capacityFlags;
    void __thiscall FUN_00cd1d80(void* allocator, int index, int removeCount, const int* source, int insertCount);
};
extern void __cdecl FUN_00c908c0(void* allocator, void* array, int newCapacity, int elementSize);
extern void __cdecl FUN_00d2cc70(void* dest, const void* src, unsigned int byteCount);
void FNVArray::FUN_00cd1d80(void* allocator, int index, int removeCount, const int* source, int insertCount) {
    int resizedCount = (m_size - removeCount) + insertCount;
    int p = (m_size - index) - removeCount;
    int cnt = m_capacityFlags & 0x3fffffff;
    if (cnt < resizedCount) {
        cnt += cnt;
        if (resizedCount >= cnt) cnt = resizedCount;
        FUN_00c908c0(allocator, this, cnt, 4);
    }
    FUN_00d2cc70(m_data + (index + insertCount), m_data + (index + removeCount), p * 4);
    int* trailingCount = m_data + index;
    for (int i = 0; i < insertCount; ++i) trailingCount[i] = source[i];
    m_size = resizedCount;
}
