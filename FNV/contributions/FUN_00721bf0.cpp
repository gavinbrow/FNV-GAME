extern "C" char str_01070244[];
const char* __cdecl FUN_00a00940(const char*, int);
struct TileLink { bool __thiscall FUN_00a01230(const char*); };
struct TargetMenu {
    int unk00; int unk04; int unk08; int unk0c;
    TileLink* selected;
    bool __thiscall FUN_00724a00();
    bool __thiscall FUN_007242f0(TileLink*);
    void __thiscall FUN_00724ab0();
    bool __thiscall FUN_00721bf0(TileLink*);
};
bool TargetMenu::FUN_00721bf0(TileLink* item)
{
    if (FUN_00724a00() &&
        (item == 0 || (FUN_007242f0(item) &&
        item->FUN_00a01230(FUN_00a00940(str_01070244, -1))))) {
        selected = item;
        FUN_00724ab0();
        return true;
    } else {
        return false;
    }
}
