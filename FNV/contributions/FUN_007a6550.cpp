extern "C" char str_01070244[];
int __cdecl FUN_00a00940(const char*, int);

struct FUN_00a01230_shell {
    bool __thiscall FUN_00a01230(int);
};

struct FUN_007a6550_shell {
    int unk00;
    int unk04;
    int unk08;
    FUN_00a01230_shell* target;

    bool __thiscall FUN_007a6550();
};

bool FUN_007a6550_shell::FUN_007a6550()
{
    static int value = FUN_00a00940(str_01070244, -1);
    return target != 0 && target->FUN_00a01230(value);
}