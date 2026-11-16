struct TESObjectWrapper
{
    void* vftable;
    unsigned int unknown_1;
    unsigned int unknown_2;
    unsigned int unknown_3;
    unsigned int unknown_4;
    unsigned int unknown_5;
    unsigned int unknown_6;
    unsigned int flags;
    void FUN_0050f9a0(unsigned int value);
};
// @fnv 0x0050f9a0
void TESObjectWrapper::FUN_0050f9a0(unsigned int value)
{
    flags = value;
}
