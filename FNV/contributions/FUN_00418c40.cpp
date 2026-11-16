struct Payload_00418c40 {
    ~Payload_00418c40();
};

struct ExtraHolder_00418c40 : public BSExtraData {
    Payload_00418c40* pData;
    ExtraHolder_00418c40(Payload_00418c40* data);
};

struct FUN_00418c40_shell : public ExtraDataList {
    ExtraHolder_00418c40* FUN_00418c40(Payload_00418c40* data);
};

ExtraHolder_00418c40* FUN_00418c40_shell::FUN_00418c40(Payload_00418c40* data)
{
    ExtraHolder_00418c40* extra =
        static_cast<ExtraHolder_00418c40*>(GetExtraData(0x10));
    if (extra) {
        delete extra->pData;
        extra->pData = data;
        return extra;
    }

    extra = new ExtraHolder_00418c40(data);
    AddExtra(extra);
    return extra;
}