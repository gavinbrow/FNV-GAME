struct FnvCpu_FUN_00d76d80_CpuTarget { void FUN_00d81340(); };
struct FnvCpu_FUN_00d76d80_CpuOwner {
    unsigned int unk00;
    unsigned int unk04;
    FnvCpu_FUN_00d76d80_CpuTarget* target;
    void FUN_00d76d80();
};
void FnvCpu_FUN_00d76d80_CpuOwner::FUN_00d76d80()
{
    target->FUN_00d81340();
}
