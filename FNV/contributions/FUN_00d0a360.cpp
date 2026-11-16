struct FUN_00d0a360_Arg {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
};

struct FUN_00d0a360_Owner {
    int unk00;
    int unk04;
    unsigned char unk08;
    unsigned char unk09;

    void __thiscall FUN_00d0a360(int arg);
};

void __thiscall FUN_00d0a360_Owner::FUN_00d0a360(int arg) {
    FUN_00d0a360_Arg* p = reinterpret_cast<FUN_00d0a360_Arg*>(arg);
    if (p->unk10 != 0) {
        if (unk09 == 0) {
            unk08 = 1;
        } else {
            reinterpret_cast<FUN_00d0a270_StandIn*>(reinterpret_cast<char*>(this) - 0x18)->FUN_00d0a270(arg);
        }
    }
}
