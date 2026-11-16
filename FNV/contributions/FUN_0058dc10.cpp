struct FUN_00483630_Base : public TESForm {
    virtual ~FUN_00483630_Base();
};
struct FUN_00483710_Member : public DecalData {
    ~FUN_00483710_Member();
};
struct FUN_0058dc10 : public FUN_00483630_Base, public TESModel {
    BGSImpactData__IMPACT_DATA_DATA Data;
    BGSTextureSet* pDecalTextureSet;
    TESSound* pSound1;
    TESSound* pSound2;
    FUN_00483710_Member DData;
    virtual ~FUN_0058dc10();
};
FUN_0058dc10::~FUN_0058dc10() {}
