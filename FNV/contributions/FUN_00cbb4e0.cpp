#include <emmintrin.h>
struct CbbName {
    char* value;
    void FUN_00cb0c10(const char* text);
};
struct FUN_00cbb4e0 {
    void* unk00;
    unsigned short unk04;
    unsigned short unk06;
    void* unk08;
    void* unk0C;
    unsigned int unk10;
    CbbName m_name;
    void* m_entity;
    unsigned int unk1C;
    hkVector4 m_positionInRbLocal;
    hkVector4 m_mousePositionInWorld;
    hkReal m_springDamping;
    hkReal m_springElasticity;
    hkReal m_maxRelativeForce;
    hkReal m_objectDamping;
    unsigned int m_shapeKey;
    hkArray<char> m_applyCallbacks;
    void FUN_00d2b260(int arg, int zero);
    FUN_00cbb4e0(int arg);
};
extern float DAT_01016248, DAT_01017870, DAT_0101b2d0, DAT_0101ffc0;
extern int DAT_010c8e94;
FUN_00cbb4e0::FUN_00cbb4e0(int arg) {
    this->FUN_00d2b260(arg,0);
    m_springDamping = DAT_01016248;
    unk00 = (void*)&DAT_010c8e94;
    m_springElasticity = DAT_01017870;
    __m128 zero = _mm_setzero_ps();
    m_maxRelativeForce = DAT_0101b2d0;
    m_objectDamping = DAT_0101ffc0;
    *(char* volatile*)&m_applyCallbacks.m_data = 0;
    *(volatile int*)&m_applyCallbacks.m_size = 0;
    *(volatile int*)&m_applyCallbacks.m_capacityAndFlags = 0x80000000;
    _mm_store_ps((float*)&m_positionInRbLocal, zero);
    _mm_store_ps((float*)&m_mousePositionInWorld, zero);
    m_shapeKey = 0xFFFFFFFF;
    m_name.FUN_00cb0c10("hkpMouseSpringAction");
}