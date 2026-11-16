#include <xmmintrin.h>
extern int DAT_010cfb34;

struct HeightFieldSource;
struct HeightFieldVtable {
    void* v00; void* v04; void* v08; void* v0c; void* v10;
    void* v14; void* v18; void* v1c; void* v20; void* v24;
    void* v28; void* v2c; void* v30;
    float (__thiscall *GetHeightAt)(HeightFieldSource*, int, int);
    void (__thiscall *GetTriangleFlip)(HeightFieldSource*, unsigned char*);
};
struct HeightFieldSource {
    HeightFieldVtable* vtable;
    unsigned short m_memSizeAndFlags;
    volatile short m_referenceCount;
    volatile unsigned int m_userData;
    volatile unsigned int m_type;
    int m_xRes;
    int m_zRes;
    float m_heightCenter;
    unsigned char m_useProjectionBasedHeight;
    volatile unsigned char m_heightfieldType;
    unsigned short m_stitchingMode;
    __m128 m_intToFloatScale;
    __m128 m_floatToIntScale;
    __m128 m_floatToIntOffsetFloorCorrected;
    __m128 m_extents;
};
struct FUN_00d49750 {
    int* volatile vtable;
    unsigned short m_memSizeAndFlags;
    volatile short m_referenceCount;
    volatile unsigned int m_userData;
    volatile unsigned int m_type;
    int m_xRes;
    int m_zRes;
    float m_heightCenter;
    unsigned char m_useProjectionBasedHeight;
    volatile unsigned char m_heightfieldType;
    unsigned short m_stitchingMode;
    __m128 m_intToFloatScale;
    __m128 m_floatToIntScale;
    __m128 m_floatToIntOffsetFloorCorrected;
    __m128 m_extents;
    float* m_storageData;
    unsigned char m_triangleFlip;
    unsigned int m_storageCapacity;
    unsigned int m_bufferOptions;
    unsigned char m_initialized;

    FUN_00d49750(HeightFieldSource* source);
};
FUN_00d49750::FUN_00d49750(HeightFieldSource* source)
    : m_referenceCount(1)
{
    m_userData = 0;
    m_type = 13;
    vtable = &DAT_010cfb34;
    m_heightfieldType = 0;
    m_xRes = source->m_xRes;
    m_zRes = source->m_zRes;
    unsigned char flip;
    source->vtable->GetTriangleFlip(source, &flip);
    m_triangleFlip = flip;
    m_heightCenter = source->m_heightCenter;
    m_intToFloatScale = source->m_intToFloatScale;
    m_floatToIntScale = source->m_floatToIntScale;
    m_floatToIntOffsetFloorCorrected = source->m_floatToIntOffsetFloorCorrected;
    m_extents = source->m_extents;
    m_storageData = new float[m_xRes * m_zRes];
    m_initialized = 1;
    for (int row = 0; row < m_zRes; ++row) {
        for (int column = 0; column < m_xRes; ++column) {
            float sampledHeight = source->vtable->GetHeightAt(source, column, row);
            m_storageData[row * m_xRes + column] = sampledHeight;
        }
    }
}