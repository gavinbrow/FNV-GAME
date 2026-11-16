struct FUN_0059a4f0 : TESBoundObject, TESFullName, TESModelTextureSwap, TESIcon, BGSMessageIcon, TESValueForm, TESScriptableForm, BGSPickupPutdownSounds
{
    bool bIsActive;
    TESTexture faceTexture;
    TESTexture backTexture;
    CARAVANCARDDATA data;
    virtual ~FUN_0059a4f0();
};

FUN_0059a4f0::~FUN_0059a4f0()
{
    static_cast<CardOwner0059*>(static_cast<void*>(this))->FUN_0059a620();
}
