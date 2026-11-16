struct FUN_004855a0_shell { void FUN_004855a0(); };
struct FUN_00487010_shell { void FUN_00487010(); };
struct FUN_00483710_shell { void FUN_00483710(); };
struct FUN_00485e20_shell { void FUN_00485e20(int, int); };
struct FUN_00485680_shell { void FUN_00485680(); };
unsigned char __cdecl FUN_00401500();

struct FUN_005a7a90_shell {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    void FUN_005a7a90();
};

void FUN_005a7a90_shell::FUN_005a7a90()
{
    ((FUN_004855a0_shell*)this)->FUN_004855a0();
    ((FUN_00487010_shell*)((char*)this + 0x18))->FUN_00487010();
    if (FUN_00401500())
        ((FUN_00483710_shell*)((char*)this + 0x24))->FUN_00483710();
    ((FUN_00485e20_shell*)this)->FUN_00485e20((int)((char*)this + 0x24), 1);
    if (FUN_00401500())
        ((FUN_00483710_shell*)((char*)this + 0x24))->FUN_00483710();
    ((FUN_00485680_shell*)this)->FUN_00485680();
}