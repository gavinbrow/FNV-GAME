extern int DAT_01268194;

struct ActorBase {
    virtual ~ActorBase();
};
struct FUN_00c8a720 : ActorBase {
    virtual ~FUN_00c8a720();
    void FUN_00c876a0();
};
FUN_00c8a720::~FUN_00c8a720()
{
    FUN_00c876a0();
    --DAT_01268194;
}
