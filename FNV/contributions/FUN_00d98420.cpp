struct CpuScalar {
    unsigned int unk00;
    float value;
};
struct CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    CpuScalar* value;
    float FUN_00d98420();
};
float CpuObject::FUN_00d98420()
{
    return value->value;
}
