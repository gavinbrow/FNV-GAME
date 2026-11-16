struct FnvCpu_FUN_00d36ce0_CpuCallData { void* descriptor; float bound; unsigned int value; };
extern float DAT_0104da48;
extern unsigned char DAT_010ce7fc;
struct FnvCpu_FUN_00d36ce0_CpuObject {
    void FUN_00d36940(void*, void*, unsigned int, FnvCpu_FUN_00d36ce0_CpuCallData*);
    void FUN_00d36ce0(void*, void*, unsigned int, unsigned int);
};
void FnvCpu_FUN_00d36ce0_CpuObject::FUN_00d36ce0(void* first, void* second, unsigned int third, unsigned int fourth)
{
    FnvCpu_FUN_00d36ce0_CpuCallData data;
    data.value = fourth;
    data.bound = DAT_0104da48;
    data.descriptor = &DAT_010ce7fc;
    FUN_00d36940(second, first, third, &data);
}
