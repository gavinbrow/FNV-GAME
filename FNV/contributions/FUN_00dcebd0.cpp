template<typename T> static __forceinline void CopyElements(T* dest, const T* src, int count) { for(int index = 0; index < count; ++index) dest[index] = src[index]; }
struct FUN_00dcebd0_Allocator {
    virtual ~FUN_00dcebd0_Allocator();
    virtual void unknown04();
    virtual void unknown08();
    virtual void* bufAlloc(int& requestedBytes);
    virtual void bufFree(void* buffer, int byteCount);
};
struct FUN_00dcebd0_Router {
    void* m_unknown00;
    void* m_unknown04;
    void* m_unknown08;
    void* m_unknown0c;
    FUN_00dcebd0_Allocator* m_allocator;
};
FUN_00dcebd0_Router* __cdecl FUN_00c85750();

struct FUN_00dcebd0_Class {
    void* m_vtable;
    unsigned short m_memSizeAndFlags;
    short m_referenceCount;
    unsigned int m_userData;
    unsigned int m_type;
    int m_reserved10;
    unsigned char m_disableWelding;
    unsigned char m_collectionType;
    unsigned short m_reserved16;
    int m_reserved18;
    int m_reserved1c;
    float m_scalingX, m_scalingY, m_scalingZ, m_scalingW;
    int m_numBitsForSubpartIndex;
    void* m_subpartsData;
    int m_subpartsSize;
    int m_subpartsCapacity;
    void* m_weldingInfoData;
    int* m_data;
    int m_size;
    int m_capacityAndFlags;

    void FUN_00d06290(const FUN_00dcebd0_Class& source);
    void FUN_00dcebd0(const FUN_00dcebd0_Class& source);
};
void FUN_00dcebd0_Class::FUN_00dcebd0(const FUN_00dcebd0_Class& source)
{
    FUN_00d06290(source);
    FUN_00dcebd0_Allocator* allocator = FUN_00c85750()->m_allocator;
    int capacity = m_capacityAndFlags & 0x3fffffff;
    if (capacity < source.m_size) {
        if ((m_capacityAndFlags & 0x80000000u) == 0) {
            allocator->bufFree(m_data, capacity * sizeof(int));
        }
        int bytes = source.m_size * sizeof(int);
        m_data = static_cast<int*>(allocator->bufAlloc(bytes));
        m_capacityAndFlags = bytes / 4;
    }
    m_size = source.m_size;
    CopyElements(m_data, source.m_data, m_size);
}