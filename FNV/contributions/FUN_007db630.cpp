struct FUN_007db630_Entry {
    int unk00;
    int unk04;
    bool FUN_005f65d0(int* value);
};
struct FUN_007db630_Owner {
    int unk00;
    FUN_007db630_Entry entries[6];
    int FUN_007db630(int value);
};
void __cdecl FUN_007dc0a0(int* value);
int FUN_007db630_Owner::FUN_007db630(int value)
{
    int index = 0;
    for (; index < 6; FUN_007dc0a0(&index)) {
        if (entries[index].FUN_005f65d0(&value))
            return index;
    }
    return 6;
}

