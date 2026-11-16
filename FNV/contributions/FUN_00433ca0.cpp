struct FUN_00433ca0 : public BSExtraData
{
    BSSimpleList<void*> kList;
    FUN_00433ca0();
    virtual ~FUN_00433ca0();
};

FUN_00433ca0::FUN_00433ca0()
    : BSExtraData(0x57), kList()
{
}