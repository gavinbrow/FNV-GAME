struct SearchContext {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    SearchContext();
    ~SearchContext();
    bool FUN_006bbd30(void* owner, int first, int second);
};
struct NavMeshSearch {
    bool FUN_00698f40(int first, int second);
};
bool NavMeshSearch::FUN_00698f40(int first, int second)
{
    SearchContext query;
    bool result = query.FUN_006bbd30(this, first, second);
    return result;
}
