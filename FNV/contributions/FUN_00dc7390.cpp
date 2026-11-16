struct FnvCpu_FUN_00dc7390_CpuTarget { void FUN_00dc9240(); };
struct FnvCpu_FUN_00dc7390_CpuOwner {
    unsigned int unk00;
    unsigned int unk04;
    FnvCpu_FUN_00dc7390_CpuTarget* target;
    void FUN_00dc7390();
};
void FnvCpu_FUN_00dc7390_CpuOwner::FUN_00dc7390()
{
    target->FUN_00dc9240();
}
