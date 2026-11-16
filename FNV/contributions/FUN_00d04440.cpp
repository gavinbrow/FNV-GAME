struct FnvCpu_FUN_00d04440_CpuScalar {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    int value;
};
struct FnvCpu_FUN_00d04440_CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    FnvCpu_FUN_00d04440_CpuScalar* value;
    int FUN_00d04440();
};
int FnvCpu_FUN_00d04440_CpuObject::FUN_00d04440()
{
    return value->value;
}
