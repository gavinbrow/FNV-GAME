struct FUN_00a530a0_shell
{
    int unk00;
    int unk04;
    int unk08;
    volatile unsigned char unk0c;
    int unk10;

    unsigned char __thiscall FUN_00a530a0(int unused);
};

extern unsigned char DAT_0109a914;

unsigned char __thiscall FUN_00a530a0_shell::FUN_00a530a0(int unused)
{
    if (unk10 != 0)
        return 0;

    return unk0c != DAT_0109a914;
}