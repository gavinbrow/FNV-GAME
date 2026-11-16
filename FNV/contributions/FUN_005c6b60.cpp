extern "C" float DAT_0103b2d0;

struct FUN_005c6b60_ActorValueOwner
{
    virtual void Unknown00();
    virtual void Unknown04();
    virtual void Unknown08();
    virtual float GetActorValue(int);
    virtual void Unknown10();
    virtual void Unknown14();
    virtual void Unknown18();
    virtual void Unknown1C();
    virtual float GetBaseActorValue(int);
};

class FUN_005c6b60_Actor : public Actor
{
public:
    virtual void Unknown58();
    virtual void Unknown5C();
    virtual void Unknown60();
    virtual void Unknown64();
    virtual void Unknown68();
    virtual void Unknown6C();
    virtual bool IsActor();
    void FUN_0088b740(int, float);
};

bool __cdecl FUN_005c6b60(void*, void*, FUN_005c6b60_Actor* actor)
{
    if (actor != 0 && actor->IsActor())
    {
        FUN_005c6b60_Actor* localActor2 = actor;
        float current = ((FUN_005c6b60_ActorValueOwner*)((char*)localActor2 + 0xa4))->GetActorValue(16);
        float base = ((FUN_005c6b60_ActorValueOwner*)((char*)localActor2 + 0xa4))->GetBaseActorValue(16);
        float differenceVal = 0.0f;
        differenceVal = base - current;
        localActor2->FUN_0088b740(16, differenceVal);
        localActor2->FUN_0088b740(29, DAT_0103b2d0);
        localActor2->FUN_0088b740(30, DAT_0103b2d0);
        localActor2->FUN_0088b740(27, DAT_0103b2d0);
        localActor2->FUN_0088b740(28, DAT_0103b2d0);
        localActor2->FUN_0088b740(25, DAT_0103b2d0);
        localActor2->FUN_0088b740(26, DAT_0103b2d0);
        localActor2->FUN_0088b740(31, DAT_0103b2d0);
    }
    return true;
}

