struct CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    float value;
    void FUN_00e47430(float input);
};
void CpuObject::FUN_00e47430(float input)
{
    value = input;
}
