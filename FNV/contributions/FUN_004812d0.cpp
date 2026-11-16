struct TESModel
{
    unsigned int GetModelLength() const;
};
struct BipedModelAccessor
{
    unsigned int unknown;
    TESModel model;
    unsigned int FUN_004812d0();
};
// @fnv 0x004812d0
unsigned int BipedModelAccessor::FUN_004812d0()
{
    return model.GetModelLength();
}
