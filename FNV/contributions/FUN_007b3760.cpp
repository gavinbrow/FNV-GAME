struct Trait {
    int FUN_0084e3a0();
    void __thiscall FUN_00a0a270(float value, unsigned int update);
};
struct TileFor3760 {
    void __thiscall FUN_00700320(unsigned int id, int value);
    Trait* __thiscall FUN_00a00f30(unsigned int id);
};
struct MenuOptionFor3760 {
    TileFor3760* tile;
    int __thiscall FUN_007b3740();
    void __thiscall FUN_007b3840(int& minValue, int& maxValue);
    bool __thiscall FUN_007b3760(int value);
};

bool MenuOptionFor3760::FUN_007b3760(int value)
{
    if (tile != 0) {
        int currentValue = FUN_007b3740();
        int minValue, maxValue;
        FUN_007b3840(minValue, maxValue);
        if (value < minValue)
            value = minValue;
        if (value > maxValue)
            value = maxValue;
        if (currentValue != value) {
            tile->FUN_00700320(0x1005, value);
            Trait* trait = tile->FUN_00a00f30(0x1009);
            if (trait->FUN_0084e3a0() == 0)
                trait->FUN_00a0a270((float)value, 1);
            return true;
        }
    }
    return false;
}