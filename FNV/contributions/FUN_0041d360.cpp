struct ExtraData_0x2f : public BSExtraData {
    int unk0C;
};

struct FUN_0041d360_shell : public ExtraDataList {
    int FUN_0041d360();
};

int FUN_0041d360_shell::FUN_0041d360() {
    ExtraData_0x2f* pExtra = (ExtraData_0x2f*)GetExtraData(0x2f);
    if (pExtra) {
        return pExtra->unk0C;
    } else {
        return -1;
    }
}
