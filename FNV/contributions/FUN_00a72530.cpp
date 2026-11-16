struct FUN_00aa4060_owner
{
    void __thiscall FUN_00aa4060(unsigned int value);
};

extern FUN_00aa4060_owner DAT_011f6238;

class FUN_00a72530_owner
{
public:
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned char unk0c;

    void __thiscall FUN_00a72530(unsigned int value);
};

void __thiscall FUN_00a72530_owner::FUN_00a72530(unsigned int value)
{
    if (value == 0 && unk0c != 0)
        value = unk08;

    DAT_011f6238.FUN_00aa4060(value);
}