struct FUN_00459920_reference {
    bool FUN_00450ff0();
    void FUN_005571a0(int changeFlag);
};
struct FUN_00459920_grid {
    FUN_00459920_reference** FUN_004ba490(unsigned int column, unsigned int row);
};
struct FUN_00459920_shell {
    void* unk00;
    void* unk04;
    FUN_00459920_grid* referenceGrid;
    FUN_00459920_reference* FUN_005f36f0();
    void FUN_00459920();
};
void FUN_00459920_shell::FUN_00459920()
{
    if (!g_dataHandler)
        return;

    if (FUN_005f36f0() && FUN_005f36f0()->FUN_00450ff0())
        FUN_005f36f0()->FUN_005571a0(0);

    for (unsigned int column = 0; column < static_cast<unsigned int>(*g_011c63cc.Int()); ++column) {
        for (unsigned int row = 0; row < static_cast<unsigned int>(*g_011c63cc.Int()); ++row) {
            FUN_00459920_reference* object;
            FUN_00459920_reference** entry = referenceGrid->FUN_004ba490(column, row);
            object = *entry;
            if (object && object->FUN_00450ff0())
                object->FUN_005571a0(0);
        }
    }
}