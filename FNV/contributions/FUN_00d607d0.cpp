struct FnvCpu_FUN_00d607d0_CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned char value;
    unsigned char* FUN_00d607d0(unsigned char* output);
};
unsigned char* FnvCpu_FUN_00d607d0_CpuObject::FUN_00d607d0(unsigned char* output)
{
    *output = value;
    return output;
}
