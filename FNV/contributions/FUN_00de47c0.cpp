struct CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    float value;
    void FUN_00de47c0(float input);
};
void CpuObject::FUN_00de47c0(float input)
{
    value = input;
}
