extern "C" char str_01070244[];
int __cdecl FUN_00a00940(const char* name, int value);
struct Item_00724430 {
    bool __thiscall FUN_00a01230(int value);
};
struct Owner_00724430 {
    int unk00;
    int unk04;
    int unk08;
    Item_00724430* item;
    bool __thiscall FUN_00724430();
};
bool Owner_00724430::FUN_00724430() {
    static int selectedValue = FUN_00a00940(str_01070244, -1);
    return item != 0 && item->FUN_00a01230(selectedValue);
}