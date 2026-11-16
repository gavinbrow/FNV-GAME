
extern int DAT_01268188;
extern int DAT_0108febc;
struct FUN_00c87c30 { void* vtable; int unk04; int unk08; FUN_00c87c30(); };
struct InitializedField { int value; InitializedField() : value(0) {} ~InitializedField(); };
struct FUN_00cb99a0 : FUN_00c87c30 {
    InitializedField unk0c;
    FUN_00cb99a0(char* source);
    void FUN_00c89dd0(char* source);
};
FUN_00cb99a0::FUN_00cb99a0(char* source) : FUN_00c87c30(), unk0c()
{
    vtable = &DAT_0108febc;
    FUN_00c89dd0(source ? source + 4 : 0);
    ++DAT_01268188;
}
