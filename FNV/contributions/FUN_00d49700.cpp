struct FUN_00d248a0 {
    FUN_00d248a0(int resolution, int mode);
    virtual ~FUN_00d248a0();
    unsigned short m_memSizeAndFlags;
    short m_referenceCount;
    unsigned long m_userData;
    unsigned int m_shapeType;
    int m_xResolution;
    int m_zResolution;
    float m_heightCenter;
    bool m_useProjectionBasedHeight;
    unsigned char m_heightfieldType;
    unsigned char m_reserved1e;
    unsigned char m_reserved1f;
    hkVector4 m_intToFloatScale;
    hkVector4 m_floatToIntScale;
    hkVector4 m_floatToIntOffsetFloorCorrected;
    hkVector4 m_extents;
};
struct FUN_00d49700 : public FUN_00d248a0 {
    int* values;
    bool cleared;
    unsigned char unk65;
    unsigned char unk66;
    unsigned char unk67;
    int capacity;
    float scale;
    bool initialized;
    FUN_00d49700(int resolution, int* source, float value);
    virtual ~FUN_00d49700();
};
FUN_00d49700::FUN_00d49700(int resolution, int* source, float value)
 : FUN_00d248a0(resolution, 0) {
    const int& zResolution = m_zResolution;
    cleared = false;
    double convertedResolution(zResolution);
    initialized = false;
    int* inputValues = (int*)*source;
    values = inputValues;
    capacity = static_cast<int>(convertedResolution - 1.0);
    scale = value;
}