struct BSSoundHandle { unsigned int unk00; unsigned int unk04; unsigned int unk08; BSSoundHandle(); BSSoundHandle& operator=(const BSSoundHandle&); ~BSSoundHandle(); };
struct BSSoundHandleEx { BSSoundHandle base; ~BSSoundHandleEx(); bool Play(bool); };
struct BSAudio { static BSAudio* GetSingleton(); BSSoundHandleEx GetSoundHandleByEditorID(const char*, unsigned int); };
struct GlobalObject_0044f440 { float* Float(); };
extern GlobalObject_0044f440 g_011db288;
extern bool g_burstSoundEnabled;
struct FUN_007fa0f0_Class {
    unsigned int unk000;
    unsigned int unk004;
    unsigned int unk008;
    unsigned int unk00C;
    unsigned int unk010;
    unsigned int unk014;
    unsigned int unk018;
    unsigned int unk01C;
    unsigned int unk020;
    unsigned int unk024;
    unsigned int unk028;
    unsigned int unk02C;
    unsigned int unk030;
    unsigned int unk034;
    unsigned int unk038;
    unsigned int unk03C;
    unsigned int unk040;
    unsigned int unk044;
    unsigned int unk048;
    unsigned int unk04C;
    unsigned int unk050;
    unsigned int unk054;
    unsigned int unk058;
    unsigned int unk05C;
    unsigned int unk060;
    unsigned int unk064;
    unsigned int unk068;
    unsigned int unk06C;
    unsigned int unk070;
    unsigned int unk074;
    unsigned int unk078;
    unsigned int unk07C;
    unsigned int unk080;
    unsigned int unk084;
    unsigned int unk088;
    unsigned int unk08C;
    unsigned int unk090;
    unsigned int unk094;
    unsigned int unk098;
    unsigned int unk09C;
    unsigned int unk0A0;
    unsigned int unk0A4;
    unsigned int unk0A8;
    unsigned int unk0AC;
    unsigned int unk0B0;
    unsigned int unk0B4;
    unsigned int unk0B8;
    unsigned int unk0BC;
    unsigned int unk0C0;
    unsigned int unk0C4;
    unsigned int unk0C8;
    unsigned int unk0CC;
    unsigned int unk0D0;
    unsigned int unk0D4;
    unsigned int unk0D8;
    unsigned int unk0DC;
    unsigned int unk0E0;
    unsigned int unk0E4;
    unsigned int unk0E8;
    unsigned int unk0EC;
    unsigned int unk0F0;
    unsigned int unk0F4;
    unsigned int unk0F8;
    unsigned int unk0FC;
    unsigned int unk100;
    unsigned int unk104;
    unsigned int unk108;
    unsigned int unk10C;
    unsigned int unk110;
    unsigned int unk114;
    unsigned int unk118;
    unsigned int unk11C;
    float unk120;
    float unk124;
    float unk128;
    float unk12c;
    float values[1];
    void __thiscall FUN_007fa0f0(int index, bool play);
};
void FUN_007fa0f0_Class::FUN_007fa0f0(int index, bool play) {
    if (unk120 != values[index]) {
        unk120 = values[index];
        unk12c = *g_011db288.Float();
        if (g_burstSoundEnabled && play) {
            BSSoundHandleEx handle;
            handle = BSAudio::GetSingleton()->GetSoundHandleByEditorID("UIPipBoyTab", 0x121);
            handle.Play(false);
        }
    }
}


