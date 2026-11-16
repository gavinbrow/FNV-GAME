struct FnvCpu_FUN_00d34b00_CpuCallData { void* descriptor; float bound; unsigned int value; };
extern float DAT_0104da48;
extern unsigned char DAT_010ce7fc;
struct FnvCpu_FUN_00d34b00_CpuObject {
    void FUN_00d33b70(void*, void*, unsigned int, FnvCpu_FUN_00d34b00_CpuCallData*);
    void FUN_00d34b00(void*, void*, unsigned int, unsigned int);
};
void FnvCpu_FUN_00d34b00_CpuObject::FUN_00d34b00(void* first, void* second, unsigned int third, unsigned int fourth)
{
    FnvCpu_FUN_00d34b00_CpuCallData data;
    data.value = fourth;
    data.bound = DAT_0104da48;
    data.descriptor = &DAT_010ce7fc;
    FUN_00d33b70(second, first, third, &data);
}
