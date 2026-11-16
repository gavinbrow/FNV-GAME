struct TargetInterface {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0c(int arg);
};

struct FUN_008b3a20_shell {
    int unk000, unk004, unk008, unk00C;
    int unk010, unk014, unk018, unk01C;
    int unk020, unk024, unk028, unk02C;
    int unk030, unk034, unk038, unk03C;
    int unk040, unk044, unk048, unk04C;
    int unk050, unk054, unk058, unk05C;
    int unk060, unk064, unk068, unk06C;
    int unk070, unk074, unk078, unk07C;
    int unk080, unk084, unk088, unk08C;
    int unk090, unk094, unk098, unk09C;
    int unk0A0, unk0A4, unk0A8, unk0AC;
    int unk0B0, unk0B4, unk0B8, unk0BC;
    int unk0C0, unk0C4, unk0C8, unk0CC;
    int unk0D0, unk0D4, unk0D8, unk0DC;
    int unk0E0, unk0E4, unk0E8, unk0EC;
    int unk0F0, unk0F4, unk0F8, unk0FC;
    int unk100, unk104, unk108, unk10C;
    int unk110, unk114, unk118, unk11C;
    int unk120, unk124, unk128, unk12C;
    int unk130, unk134, unk138, unk13C;
    int unk140, unk144, unk148, unk14C;
    int unk150, unk154, unk158, unk15C;
    int unk160, unk164, unk168, unk16C;
    int unk170, unk174, unk178, unk17C;
    int unk180, unk184, unk188, unk18C;
    TargetInterface* unk190;

    void FUN_008b3a20(int arg);
};

void FUN_008b3a20_shell::FUN_008b3a20(int arg)
{
    unk190->v0c(arg);
}
