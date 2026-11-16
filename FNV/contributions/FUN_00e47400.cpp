struct FnvCpu_FUN_00e47400_CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned char value;
    unsigned char* FUN_00e47400(unsigned char* output);
};
unsigned char* FnvCpu_FUN_00e47400_CpuObject::FUN_00e47400(unsigned char* output)
{
    *output = value;
    return output;
}
