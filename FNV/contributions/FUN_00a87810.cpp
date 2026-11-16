class FUN_00a74480 {
public:
    void* m_pVftable;
    FUN_00a74480(unsigned int flags);
};
extern char DAT_0109e984;
class FUN_00a87810 : public FUN_00a74480 {
public:
    FUN_00a87810(unsigned int flags);
};
FUN_00a87810::FUN_00a87810(unsigned int flags) : FUN_00a74480(flags)
{
    m_pVftable = &DAT_0109e984;
}
