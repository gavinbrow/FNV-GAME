
extern int DAT_010e9b7c;
struct IndexArray {
 void* m_data;int m_size;int m_capacityAndFlags;
 IndexArray():m_data(0),m_size(0),m_capacityAndFlags(0x80000000){}
};
struct FUN_00e61720 {
 void* m_vptr;unsigned short m_memSizeAndFlags;short m_referenceCount;
 void* m_vertexBuffer;IndexArray m_indexBuffers;void* m_material;IndexArray m_userChannels;
 FUN_00e61720(void* arg);void FUN_00e61770(void* arg);
};
FUN_00e61720::FUN_00e61720(void* arg): m_vptr(&DAT_010e9b7c),m_referenceCount(1),m_vertexBuffer(0),m_indexBuffers(),m_material(0),m_userChannels() { FUN_00e61770(arg); }
