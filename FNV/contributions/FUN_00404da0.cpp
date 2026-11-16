extern "C" unsigned char DAT_010121b4;

struct FUN_00405230_Class
{
    void FUN_00405230();
    void FUN_00404da0();
};

// @fnv 0x00404da0
void FUN_00405230_Class::FUN_00404da0()
{
    *reinterpret_cast<void**>(this) = &DAT_010121b4;
    FUN_00405230();
}
