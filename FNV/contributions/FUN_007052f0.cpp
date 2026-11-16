struct FUN_00404eb0 {
    int contextId;
    FUN_00404eb0(int category, int level, const char* sourceName, int messageId);
    ~FUN_00404eb0();
};
bool __fastcall FUN_009373f0(InterfaceManager* manager);
struct MessageSink {
    void __thiscall FUN_00775380(int a, int b, int c, int d,
                                 float value, unsigned char option);
};
extern "C" MessageSink* DAT_011d96c0;
extern "C" const char str_0106eb78[];

bool __cdecl FUN_007052f0(int a, int b, int c, int d, float value, unsigned char option) {
    FUN_00404eb0 scope(13, 1, str_0106eb78, 0x901);
    if (FUN_004b7210() && FUN_009373f0(FUN_004b7210()) && DAT_011d96c0)
        DAT_011d96c0->FUN_00775380(a, b, c, d, value, option);
    return false;
}