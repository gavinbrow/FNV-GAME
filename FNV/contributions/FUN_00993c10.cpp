struct TargetData {
    int unk00;
    int unk04;
    unsigned __int64 unk08;
};

struct TargetMember {
    void FUN_006b8310(TargetData* data);
};

struct TargetOwner {
    int unk00;
    int unk04;
    int unk08;
    TargetMember member0c;
    void FUN_00993c10(TargetData* data);
};

void TargetOwner::FUN_00993c10(TargetData* data)
{
    data->unk08 = 0;
    member0c.FUN_006b8310(data);
}