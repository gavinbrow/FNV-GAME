struct FUN_00c85d20_Class {
    void __thiscall FUN_00c85d20(bool enabled);
};

struct FUN_00c67130_First {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00c85d20_Class* unk10;
};

struct FUN_00c67130_Second {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
};

void __cdecl FUN_00c67130(FUN_00c67130_First* first, FUN_00c67130_Second* second)
{
    if (first->unk10) {
        first->unk10->FUN_00c85d20(second->unk0c != 0);
    }
}