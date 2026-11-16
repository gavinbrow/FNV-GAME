struct MenuFactory {
    Menu* FUN_00a03c90();
};
MenuFactory* __cdecl FUN_00a09030(int id);
int __cdecl FUN_00754de0(int value);

bool __cdecl FUN_00754cf0(int value) {
    MenuFactory* factory = FUN_00a09030(0x433);
    CompanionWheelMenu* menu = factory
        ? dynamic_cast<CompanionWheelMenu*>(factory->FUN_00a03c90())
        : 0;
    if (menu)
        delete menu;
    if (FUN_00754de0(value))
        return true;
    return false;
}