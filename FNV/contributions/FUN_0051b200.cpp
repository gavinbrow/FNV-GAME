struct ObjectFormBase {
    virtual ~ObjectFormBase();
    unsigned int unk04, unk08, unk0c, unk10, unk14, unk18;
    unsigned int unk1c, unk20, unk24, unk28, unk2c;
};
struct ModelTextureBase {
    virtual ~ModelTextureBase();
};
struct FUN_0051b200 : ObjectFormBase, ModelTextureBase {
    virtual ~FUN_0051b200();
    void FUN_00483710();
};
FUN_0051b200::~FUN_0051b200() {
    FUN_00483710();
}