extern float DAT_0109643c;
extern float DAT_01015f5c;
extern double DAT_010231b0;
extern double DAT_010241b0;
struct NiBlendInterpolator {
    virtual void v00();
    virtual void v01();
    virtual void v02();
    virtual void v03();
    virtual void v04();
    virtual void v05();
    virtual void v06();
    virtual void v07();
    virtual void v08();
    virtual void v09();
    virtual void v10();
    virtual void v11();
    virtual void v12();
    virtual void v13();
    virtual void v14();
    virtual void v15();
    virtual void v16();
    virtual void v17();
    virtual void v18();
    virtual void v19();
    virtual void v20();
    virtual void v21();
    virtual void v22();
    virtual void v23();
    virtual void v24();
    virtual void v25();
    virtual void v26();
    virtual void v27();
    virtual void v28();
    virtual void v29();
    virtual void v30();
    virtual void v31();
    virtual void v32();
    virtual void v33();
    virtual void v34();
    virtual void v35();
    virtual void v36();
    virtual void v37();
    virtual void v38();
    virtual void v39();
    virtual void v40();
    virtual void v41();
    virtual void v42();
    virtual void v43();
    virtual void v44();
    virtual void v45();
    virtual void v46();
    virtual void v47();
    virtual void GetTimeRange(float* minTime, float* maxTime);
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
};
struct TimeFlags { unsigned char m_unused:5; unsigned char m_bManagerControlled:1; unsigned char m_reserved:2; };
struct NiMultiTargetTimeShell : public NiMultiTargetTransformController {
    unsigned short m_usNumTargets;
    bool GetManagerControlled() const { return (reinterpret_cast<const unsigned short*>(m_padding + 4)[0] >> 5) & 1; }
    float& LoKeyTime() { return *reinterpret_cast<float*>(m_padding + 0x10); }
    float& HiKeyTime() { return *reinterpret_cast<float*>(m_padding + 0x14); }
    void FUN_00a2f8f0();
    void FUN_00a2fde0();
};
void NiMultiTargetTimeShell::FUN_00a2fde0() {
    if (!GetManagerControlled()) {
        LoKeyTime() = DAT_0109643c;
        HiKeyTime() = DAT_01015f5c;
        for (unsigned short index = 0; index < m_usNumTargets; ++index) {
            float endTime = DAT_01015f5c;
            float startTime = DAT_0109643c;
            static_cast<NiBlendInterpolator*>(m_pkBlendInterps)[index].GetTimeRange(&startTime, &endTime);
            if (startTime < LoKeyTime())
                LoKeyTime() = startTime;
            if (endTime > HiKeyTime())
                HiKeyTime() = endTime;
        }
        if (LoKeyTime() == DAT_010231b0 && HiKeyTime() == DAT_010241b0)
            FUN_00a2f8f0();
    }
}