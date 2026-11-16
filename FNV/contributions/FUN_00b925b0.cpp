
extern "C" void* __cdecl FUN_00ec61c0(void*, int, unsigned int);
extern "C" char str_010b0158;
extern "C" char str_010b5c70;
extern "C" char str_010b5c64;
extern "C" char str_010a93ec;
extern "C" char str_010a93cc;

struct RenderBuffer {
    void* typeInfo;
    unsigned int state;
    unsigned int state08;
    unsigned int state0c;
    unsigned int state10;
    unsigned int state14;
    unsigned int state18;
    unsigned int state1c;
    unsigned int state20;
    unsigned int state24;
    unsigned int state28;
    unsigned int state2c;
    unsigned int state30;
    unsigned int state34;
    unsigned int state38;
    unsigned int state3c;
    unsigned int state40;
    unsigned int state44;
    unsigned int state48;
};

struct RenderState {
    void FUN_00e7f430(unsigned int state, unsigned int value, unsigned int enabled);
};
extern "C" RenderState* __cdecl FUN_00e7f5d0();

struct GroupState {
    unsigned int unk00, unk04, unk08, unk0c, unk10, unk14;
    unsigned int unk18, unk1c, unk20, unk24, unk28, unk2c;
    RenderState* state;
};

struct RenderOwner {
    void** virtualTable;
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
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    GroupState* group;
    void FUN_00b925b0();
};

typedef void (__thiscall *ApplyState)(RenderOwner*, RenderBuffer*, RenderBuffer*, const void*, const void*, const void*);
typedef void (__thiscall *CommitState)(RenderOwner*);

void RenderOwner::FUN_00b925b0()
{
    RenderBuffer current;
    current.typeInfo = &str_010b0158;
    current.state = 0;
    FUN_00ec61c0(&current.state08, 0, 0x44);

    RenderBuffer fallback;
    fallback.typeInfo = &str_010b5c70;
    fallback.state = 0;
    FUN_00ec61c0(&fallback.state08, 0, 0x44);

    reinterpret_cast<ApplyState>(virtualTable[0x13c / sizeof(void*)])(this, &current, &fallback, &str_010b5c64, &str_010a93ec, &str_010a93cc);
    reinterpret_cast<CommitState>(virtualTable[0x14c / sizeof(void*)])(this);

    GroupState* stateOwner = group;
    if (!stateOwner->state)
        stateOwner->state = FUN_00e7f5d0();
    stateOwner->state->FUN_00e7f430(0x1b, 1, 1);

    GroupState* nextOwner = group;
    if (!nextOwner->state)
        nextOwner->state = FUN_00e7f5d0();
    nextOwner->state->FUN_00e7f430(0x13, 5, 1);

    if (!nextOwner->state)
        nextOwner->state = FUN_00e7f5d0();
    nextOwner->state->FUN_00e7f430(0x14, 6, 1);
}
