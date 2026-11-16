
struct Actor {
    void** vtbl;
    unsigned char FUN_00493bb0();
    void FUN_008a6730(Actor*);
};

struct Ref {
    Actor* FUN_00822b40();
};

struct Population {
    unsigned int FUN_005be5c0(unsigned int unused);
    Actor* FUN_00968670(unsigned int index);
};

struct World {
    Population* FUN_00717e50();
};

extern "C" World DAT_011e0e80;

struct FrenzyEffectCore {
    unsigned int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    unsigned int unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    unsigned int unk40, unk44, unk48;
    unsigned char exhausted;
    void FUN_0082c810();
    Ref* FUN_0059bb30();
    void FUN_0080ddd0();
};

typedef void (__thiscall *ActorAction)(Actor*,Actor*);
typedef unsigned char (__thiscall *ActorPredicate)(Actor*);

void FrenzyEffectCore::FUN_0080ddd0()
{
    FUN_0082c810();
    if (exhausted) return;
    {
        Actor* actor = FUN_0059bb30() ? FUN_0059bb30()->FUN_00822b40() : 0;
        if (actor != 0 && actor->FUN_00493bb0()) {
            ((ActorAction)actor->vtbl[269])(actor, 0);
            Population* group = DAT_011e0e80.FUN_00717e50();
            for (unsigned int counter=0; counter<group->FUN_005be5c0(0); counter++) {
                Actor* element = group->FUN_00968670(counter);
                if (element != actor) {
                    Actor* other = element != 0 && ((ActorPredicate)element->vtbl[64])(element) ? element : 0;
                    if (other) {
                        other->FUN_008a6730(actor);
                        if (other->FUN_00493bb0())
                            ((ActorAction)other->vtbl[269])(other, actor);
                    }
                }
            }
        }
    }
}
