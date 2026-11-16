struct GameMember {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    ~GameMember();
};
struct FUN_004876d0 {
    virtual ~FUN_004876d0();
    GameMember firstMember;
    GameMember secondMember;
    void FUN_00487770();
};
FUN_004876d0::~FUN_004876d0()
{
    FUN_00487770();
}