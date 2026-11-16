extern int DAT_010a318c;
struct FUN_00acde90_class {
    void __thiscall FUN_00acde90();
};
void FUN_00acde90_class::FUN_00acde90()
{
    *reinterpret_cast<void**>(
        reinterpret_cast<char*>(this) +
        (*reinterpret_cast<int**>(reinterpret_cast<char*>(this) - 4))[1] - 4
    ) = &DAT_010a318c;
}
