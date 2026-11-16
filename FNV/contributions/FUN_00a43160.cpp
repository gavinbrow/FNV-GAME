struct NiPoint3 { float x, y, z; };
struct NiQuaternion { float w, x, y, z; };
struct NiQuatTransform { NiPoint3 translate; NiQuaternion rotate; float scale; };
extern const NiPoint3 DAT_011a8400;
extern const NiQuaternion DAT_011f3704;
extern const float DAT_01096b8c;
extern const float DAT_0109696c;
extern const double DAT_01012070;
extern const float DAT_01015f5c;
struct NiObjectNET;
struct NiInterpolatorUpdate {
    virtual void f00(); virtual void f01(); virtual void f02(); virtual void f03();
    virtual void f04(); virtual void f05(); virtual void f06(); virtual void f07();
    virtual void f08(); virtual void f09(); virtual void f10(); virtual void f11();
    virtual void f12(); virtual void f13(); virtual void f14(); virtual void f15();
    virtual void f16(); virtual void f17(); virtual void f18(); virtual void f19();
    virtual void f20(); virtual void f21(); virtual void f22(); virtual void f23();
    virtual void f24(); virtual void f25(); virtual void f26(); virtual void f27();
    virtual void f28(); virtual void f29(); virtual void f30(); virtual void f31();
    virtual void f32(); virtual void f33(); virtual void f34();
    virtual bool Update(float, NiObjectNET*, NiQuatTransform&);
    int unk04, unk08, unk0c, unk10, unk14;
    float m_fScale;
};
struct BlendItem {
    NiInterpolatorUpdate* interpolator;
    int unk04;
    float weight;
    int unk0c, unk10;
    float time;
};
struct BSBlendInterpClass {
    void* vtbl;
    unsigned int refCount;
    float lastTime;
    unsigned char flags, count, active, single;
    int unk10;
    BlendItem* items;
    int unk18, unk1c, unk20, unk24, unk28, unk2c;
    float phase;
    bool FUN_00a43160(float time, NiObjectNET* object, NiQuatTransform& result);
};
bool BSBlendInterpClass::FUN_00a43160(float time, NiObjectNET* object, NiQuatTransform& result) {
    float total = 0.0f;
    for (unsigned char i = 0; i < count; ++i) {
        BlendItem& item = items[i];
        if (item.interpolator && item.weight > 0.0f) {
            float sampleTime = time;
            if (item.weight != 0.0f) {
                if (flags & 1) sampleTime = item.time;
                if (sampleTime != DAT_0109696c) {
                    NiQuatTransform transform = { DAT_011a8400, DAT_011f3704, DAT_01096b8c };
                    if (item.interpolator->Update(sampleTime, object, transform)) {
                        total += item.interpolator->m_fScale * item.weight;
                    }
                }
            }
        }
    }
    float& combined = phase;
    combined += total;
    if (combined > 1.0f) phase = combined - DAT_01012070;
    else if (combined < 0.0f) phase = combined + DAT_01012070;
    float* __restrict out = (float*)&result; out[7] = out[4] = out[0] = DAT_01015f5c;
    return true;
}