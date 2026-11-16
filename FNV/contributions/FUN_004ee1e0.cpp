struct FUN_00a5e930 {
    virtual void ReservedVirtual();
    ~FUN_00a5e930();
    unsigned int unk004;
    unsigned int unk008;
    unsigned int unk00c;
    unsigned int unk010;
    unsigned int unk014;
    unsigned int unk018;
    unsigned int unk01c;
    unsigned int unk020;
    unsigned int unk024;
    unsigned int unk028;
    unsigned int unk02c;
    unsigned int unk030;
    unsigned int unk034;
    unsigned int unk038;
    unsigned int unk03c;
    unsigned int unk040;
    unsigned int unk044;
    unsigned int unk048;
    unsigned int unk04c;
    unsigned int unk050;
    unsigned int unk054;
    unsigned int unk058;
    unsigned int unk05c;
    unsigned int unk060;
    unsigned int unk064;
    unsigned int unk068;
    unsigned int unk06c;
    unsigned int unk070;
    unsigned int unk074;
    unsigned int unk078;
    unsigned int unk07c;
    unsigned int unk080;
    unsigned int unk084;
    unsigned int unk088;
    unsigned int unk08c;
    unsigned int unk090;
    unsigned int unk094;
    unsigned int unk098;
    unsigned int unk09c;
    unsigned int unk0a0;
    unsigned int unk0a4;
    unsigned int unk0a8;
};
struct ListCursor {
    void* FUN_00559450();
};
struct FUN_004ee360 {
    bool FUN_004a4460();
    ListCursor* FUN_006815c0();
    void FUN_004ee8a0();
    ~FUN_004ee360();
};
struct GlobalRemovalList {
    void FUN_00905330(void** object);
};
extern GlobalRemovalList g_011c7d20;
void __cdecl FUN_004ee2e0(void* item);

struct FUN_004ee1e0 : FUN_00a5e930 {
    FUN_004ee360* entries;
    virtual ~FUN_004ee1e0();
};
FUN_004ee1e0::~FUN_004ee1e0() {
    FUN_004ee1e0* self = this;
    g_011c7d20.FUN_00905330((void**)&self);
    if (entries) {
        while (!entries->FUN_004a4460()) {
            FUN_004ee2e0(entries->FUN_006815c0()->FUN_00559450());
            entries->FUN_004ee8a0();
        }
        delete entries;
        entries = 0;
    }
}