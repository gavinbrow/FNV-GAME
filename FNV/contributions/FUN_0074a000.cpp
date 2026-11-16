
struct FNV_74A000_Item;

struct FNV_74A000_Action {
    void __thiscall FUN_00a012d0();
};

struct FNV_74A000_List {
    FNV_74A000_Item* __thiscall FUN_00559450();
    int* __thiscall FUN_0073ac90();
    FNV_74A000_Action** __thiscall FUN_006317a0(FNV_74A000_Item* item, int type, float amount, int flag);
    FNV_74A000_Item* __thiscall FUN_007b52d0(FNV_74A000_Item* item);
};

struct FNV_74A000_Slot {
    int unk00;
    FNV_74A000_List list;
};

struct FNV_74A000_Root {
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
    FNV_74A000_Slot* slots[1];
};

struct FNV_74A000_This {
    void __thiscall FUN_0074a000(int slot, float amount);
};

void FNV_74A000_This::FUN_0074a000(int slot, float amount)
{
    FNV_74A000_Item* item = reinterpret_cast<FNV_74A000_Root*>(DAT_011d917c)->slots[slot]->list.FUN_00559450();
    FNV_74A000_List* list = &reinterpret_cast<FNV_74A000_Root*>(DAT_011d917c)->slots[slot]->list;

    while (item && list && *list->FUN_0073ac90()) {
        (*list->FUN_006317a0(item, 0xfa9, amount, 1))->FUN_00a012d0();
        item = list->FUN_007b52d0(item);
    }
}
