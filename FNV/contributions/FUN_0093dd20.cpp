class ActorMover {
public:
    virtual void Unknown0();
    virtual void Unknown1();
    virtual void Unknown2();
    virtual void SetAnimationFlags(unsigned short flags);
};

class CharacterActionState : public Actor {
public:
    unsigned short FUN_008846e0();
    void FUN_0093dd20();
};

void CharacterActionState::FUN_0093dd20()
{
    unsigned short currentGroup = FUN_008846e0();
    unsigned short flags = 0;
    flags = currentGroup & 0xCC00;
    flags |= 0x0400;
    pActorMover->SetAnimationFlags(flags);
}