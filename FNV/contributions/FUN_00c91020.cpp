struct CpuScalar {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    float value;
};
struct CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    CpuScalar* value;
    float FUN_00c91020();
};
float CpuObject::FUN_00c91020()
{
    return value->value;
}
