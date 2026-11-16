struct FUN_0041cb40_extra {
    BSExtraData base;
    void* unk0C;
    void* unk10;
};

struct FUN_0041cb40_shell : public ExtraDataList {
    void* FUN_0041cb40();
};

void* FUN_0041cb40_shell::FUN_0041cb40()
{
    BSExtraData* pExtra = GetExtraData(0x19);

    if (pExtra) {
        return reinterpret_cast<FUN_0041cb40_extra*>(pExtra)->unk10;
    } else {
        return 0;
    }
}