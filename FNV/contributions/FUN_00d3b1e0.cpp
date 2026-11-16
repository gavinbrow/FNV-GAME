struct CpuCallData { void* descriptor; float bound; unsigned int value; };
extern float DAT_0104da48;
extern unsigned char DAT_010ce7fc;
struct CpuObject {
    void FUN_00d39ef0(void*, void*, unsigned int, CpuCallData*);
    void FUN_00d3b1e0(void*, void*, unsigned int, unsigned int);
};
void CpuObject::FUN_00d3b1e0(void* first, void* second, unsigned int third, unsigned int fourth)
{
    CpuCallData data;
    data.value = fourth;
    data.bound = DAT_0104da48;
    data.descriptor = &DAT_010ce7fc;
    FUN_00d39ef0(second, first, third, &data);
}
