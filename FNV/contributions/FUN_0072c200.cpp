extern const char DAT_01070244[];
extern void* __cdecl FUN_00a00940(const char* name, int fallback);

struct TileValueChecker {
    bool FUN_00a01230(void* value);
};

struct MenuTileControl {
    int menuID;
    int state;
    int selected;
    TileValueChecker* tile;

    bool FUN_0072c200();
};

bool MenuTileControl::FUN_0072c200()
{
    static void* cachedValue = FUN_00a00940(DAT_01070244, -1);
    return tile != 0 && tile->FUN_00a01230(cachedValue);
}