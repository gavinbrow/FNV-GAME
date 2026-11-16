struct SaveEntryData {
    unsigned short resourceId;
    short row;
    short column;
    unsigned short flagsLow;
    unsigned short flagsHigh;
};
struct ItemRef {
    unsigned int FUN_00846d20();
};
struct ItemManager {
    ItemRef* FUN_0084e3a0(unsigned int resourceId);
};
struct FUN_0084e3c0_Class {
    unsigned int handle;
    int row;
    int column;
    unsigned int flags;
    void FUN_0084e3c0(const SaveEntryData* data);
};
void FUN_0084e3c0_Class::FUN_0084e3c0(const SaveEntryData* data) {
    row = data->row;
    column = data->column;
    flags = *reinterpret_cast<const unsigned int*>(&data->flagsLow);
    handle = reinterpret_cast<ItemManager*>(g_BGSSaveLoadGame)->FUN_0084e3a0(data->resourceId)->FUN_00846d20();
}