struct FUN_00591a40_fallback
{
    char* data;
    unsigned short length;
    unsigned short capacity;

    void* FUN_00408da0();
};

struct TESModel
{
    void* vtable;
    FUN_00591a40_fallback modelPath;
    float radius;
    void* textureHashes;
    unsigned int textureHashCount;

    unsigned int GetModelLength() const;
};

struct TESModelTextureSwap : TESModel
{
    void* textureSwaps;
    unsigned int textureSwapCount;
};

struct TESIcon
{
    void* vtable;
    FUN_00591a40_fallback iconPath;

    unsigned int FUN_0048cee0() const;
    void* FUN_00408da0();
};

struct TESBipedModelForm
{
    void* vtable;
    unsigned int slotMask;
    unsigned int flags;
    TESModelTextureSwap models[2];
    TESModelTextureSwap groundModels[2];
    TESIcon icons[2];

    const char* FUN_00481230(int gender);
};

// @fnv 0x00481230
const char* TESBipedModelForm::FUN_00481230(int gender)
{
    if (icons[gender].FUN_0048cee0() == 0 && gender == 1)
    {
        gender = 0;
    }
    return static_cast<const char*>(icons[gender].FUN_00408da0());
}
