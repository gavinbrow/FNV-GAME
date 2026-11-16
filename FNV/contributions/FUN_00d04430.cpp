struct FnvCpu_FUN_00d04430_CpuScalar {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    int value;
};
struct FnvCpu_FUN_00d04430_CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    FnvCpu_FUN_00d04430_CpuScalar* value;
    int FUN_00d04430();
};
int FnvCpu_FUN_00d04430_CpuObject::FUN_00d04430()
{
    return value->value;
}
