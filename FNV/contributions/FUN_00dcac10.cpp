struct CpuScalar {
    unsigned int unk00;
    unsigned int unk04;
    int value;
};
struct CpuObject {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    CpuScalar* value;
    int FUN_00dcac10();
};
int CpuObject::FUN_00dcac10()
{
    return value->value;
}
