typedef unsigned int uint32;
struct AnimationHandle {
    ~AnimationHandle();
    int FUN_00726070();
    void* FUN_004459e0(unsigned int);
    int FUN_004bd7a0();
    int FUN_004bd7a0(int);
    unsigned char FUN_004bda70();
};
struct AnimationCursor {
    int* FUN_006815c0();
    AnimationCursor* FUN_00726070();
    bool FUN_005f65d0(int*);
};
struct AnimationSequenceList {
    AnimationCursor* FUN_00474a40();
};
struct AnimationSequenceFactory {
    AnimationCursor* FUN_00500940();
};
struct AnimationCollection {
    AnimationSequenceFactory* FUN_00474a40();
    int FUN_00525980(int);
};
struct AnimationData;
struct NextState;
struct AnimationLink;
struct AnimationController {
 virtual void Unknown00();
 virtual void Unknown01();
 virtual void Unknown02();
 virtual void Unknown03();
 virtual void Unknown04();
 virtual void Unknown05();
 virtual void Unknown06();
 virtual void Unknown07();
 virtual void Unknown08();
 virtual void Unknown09();
 virtual void Unknown0A();
 virtual void Unknown0B();
 virtual void Unknown0C();
 virtual void Unknown0D();
 virtual void Unknown0E();
 virtual void Unknown0F();
 virtual void Unknown10();
 virtual void Unknown11();
 virtual void Unknown12();
 virtual void Unknown13();
 virtual void Unknown14();
 virtual void Unknown15();
 virtual void Unknown16();
 virtual void Unknown17();
 virtual void Unknown18();
 virtual void Unknown19();
 virtual void Unknown1A();
 virtual void Unknown1B();
 virtual void Unknown1C();
 virtual void Unknown1D();
 virtual void Unknown1E();
 virtual void Unknown1F();
 virtual void Unknown20();
 virtual void Unknown21();
 virtual void Unknown22();
 virtual void Unknown23();
 virtual void Unknown24();
 virtual void Unknown25();
 virtual void Unknown26();
 virtual void Unknown27();
 virtual void Unknown28();
 virtual void Unknown29();
 virtual void Unknown2A();
 virtual void Unknown2B();
 virtual void Unknown2C();
 virtual void Unknown2D();
 virtual void Unknown2E();
 virtual void Unknown2F();
 virtual void Unknown30();
 virtual void Unknown31();
 virtual void Unknown32();
 virtual void Unknown33();
 virtual void Unknown34();
 virtual void Unknown35();
 virtual void Unknown36();
 virtual void Unknown37();
 virtual void Unknown38();
 virtual void Unknown39();
 virtual void Unknown3A();
 virtual void Unknown3B();
 virtual void Unknown3C();
 virtual void Unknown3D();
 virtual void Unknown3E();
 virtual void Unknown3F();
 virtual void Unknown40();
 virtual void Unknown41();
 virtual void Unknown42();
 virtual void Unknown43();
 virtual void Unknown44();
 virtual void Unknown45();
 virtual void Unknown46();
 virtual void Unknown47();
 virtual void Unknown48();
 virtual void Unknown49();
 virtual void Unknown4A();
 virtual void Unknown4B();
 virtual void Unknown4C();
 virtual void Unknown4D();
 virtual void Unknown4E();
 virtual void Unknown4F();
 virtual void Unknown50();
 virtual void Unknown51();
 virtual AnimationData* GetState();
 virtual NextState* Toggle(int);
 virtual void Unknown54();
 virtual void Unknown55();
 virtual void Unknown56();
 virtual void Unknown57();
 virtual void Unknown58();
 virtual void Unknown59();
 virtual void SetLink(AnimationLink*);
};
struct AnimationLink {
    AnimationLink(int animationId, int packedData);
    AnimationLink* FUN_004bc550(int animationId, int packedData);
    unsigned int id;
    int data;
    AnimationLink* next;
};
struct AnimationData {
    int FUN_00525980(int);
    int FUN_004bd7a0();
    int FUN_004bd7a0(int);
    AnimationData* FUN_0044ddc0();
    int unknown00;
    int unknown04;
    int unknown08;
    int unknown0C;
    int unknown10;
    int unknown14;
    int unknown18;
    int unknown1C;
    int unknown20;
    int unknown24;
    int unknown28;
    int unknown2C;
    int unknown30;
    int unknown34;
    int unknown38;
    int unknown3C;
    int unknown40;
    int unknown44;
    int unknown48;
    int unknown4C;
    int unknown50;
    int unknown54;
    int unknown58;
    int unknown5C;
    int unknown60;
    int unknown64;
    int unknown68;
    int unknown6C;
    int unknown70;
    int unknown74;
    int unknown78;
    int unknown7C;
    int unknown80;
    int unknown84;
    int unknown88;
    int unknown8C;
    int unknown90;
    int unknown94;
    int unknown98;
    int unknown9C;
    int unknownA0;
    AnimationCollection animations;
};
struct ActorAnimation : TESObjectREFR {
    AnimationController* process;
    virtual void UnknownActor90();
    virtual void UnknownActor91();
    virtual void UnknownActor92();
    virtual void UnknownActor93();
    virtual void UnknownActor94();
    virtual void UnknownActor95();
    virtual void UnknownActor96();
    virtual void UnknownActor97();
    virtual void UnknownActor98();
    virtual void UnknownActor99();
    virtual void UnknownActor9A();
    virtual void UnknownActor9B();
    virtual void UnknownActor9C();
    virtual void UnknownActor9D();
    virtual void UnknownActor9E();
    virtual void UnknownActor9F();
    virtual void UnknownActorA0();
    virtual void UnknownActorA1();
    virtual void UnknownActorA2();
    virtual void UnknownActorA3();
    virtual void UnknownActorA4();
    virtual void UnknownActorA5();
    virtual void UnknownActorA6();
    virtual void UnknownActorA7();
    virtual void UnknownActorA8();
    virtual void UnknownActorA9();
    virtual void UnknownActorAA();
    virtual void UnknownActorAB();
    virtual void UnknownActorAC();
    virtual void UnknownActorAD();
    virtual void UnknownActorAE();
    virtual void UnknownActorAF();
    virtual void UnknownActorB0();
    virtual void UnknownActorB1();
    virtual void UnknownActorB2();
    virtual void UnknownActorB3();
    virtual void UnknownActorB4();
    virtual void UnknownActorB5();
    virtual void UnknownActorB6();
    virtual void UnknownActorB7();
    virtual void UnknownActorB8();
    virtual void UnknownActorB9();
    virtual void UnknownActorBA();
    virtual void UnknownActorBB();
    virtual void UnknownActorBC();
    virtual void UnknownActorBD();
    virtual void UnknownActorBE();
    virtual void UnknownActorBF();
    virtual void UnknownActorC0();
    virtual void UnknownActorC1();
    virtual void UnknownActorC2();
    virtual void UnknownActorC3();
    virtual void UnknownActorC4();
    virtual void UnknownActorC5();
    virtual void UnknownActorC6();
    virtual void UnknownActorC7();
    virtual void UnknownActorC8();
    virtual void UnknownActorC9();
    virtual void UnknownActorCA();
    virtual void UnknownActorCB();
    virtual void UnknownActorCC();
    virtual void UnknownActorCD();
    virtual void UnknownActorCE();
    virtual void UnknownActorCF();
    virtual void UnknownActorD0();
    virtual void UnknownActorD1();
    virtual void UnknownActorD2();
    virtual void UnknownActorD3();
    virtual void UnknownActorD4();
    virtual void UnknownActorD5();
    virtual void UnknownActorD6();
    virtual void UnknownActorD7();
    virtual void UnknownActorD8();
    virtual void UnknownActorD9();
    virtual void UnknownActorDA();
    virtual void UnknownActorDB();
    virtual void UnknownActorDC();
    virtual void UnknownActorDD();
    virtual void UnknownActorDE();
    virtual void UnknownActorDF();
    virtual void UnknownActorE0();
    virtual void UnknownActorE1();
    virtual void UnknownActorE2();
    virtual void UnknownActorE3();
    virtual void UnknownActorE4();
    virtual void UnknownActorE5();
    virtual void UnknownActorE6();
    virtual void UnknownActorE7();
    virtual void UnknownActorE8();
    virtual void UnknownActorE9();
    virtual void UnknownActorEA();
    virtual void UnknownActorEB();
    virtual void UnknownActorEC();
    virtual void UnknownActorED();
    virtual void UnknownActorEE();
    virtual void UnknownActorEF();
    virtual void UnknownActorF0();
    virtual void UnknownActorF1();
    virtual void UnknownActorF2();
    virtual void UnknownActorF3();
    virtual void UnknownActorF4();
    virtual void UnknownActorF5();
    virtual void UnknownActorF6();
    virtual void UnknownActorF7();
    virtual void UnknownActorF8();
    virtual void UnknownActorF9();
    virtual void UnknownActorFA();
    virtual void ApplyAnimation(AnimationData*, int, unsigned char, int, bool);
    void* FUN_00576260(int id, int flags);
    int FUN_004c8f30(int);
    int FUN_004bfb70(int,int);
    bool FUN_008a16d0();
    void __thiscall FUN_009462c0(unsigned char allowTransition, unsigned char skipIfPlayable);
};
extern int DAT_011dea3c;
extern void* __cdecl FUN_004bf220(ActorAnimation*);
extern void* __cdecl FUN_00401000(unsigned int);
struct NextState { void FUN_006ecd40(); };
extern int __cdecl FUN_0044ddc0(void*);
void __thiscall ActorAnimation::FUN_009462c0(unsigned char allowTransition, unsigned char skipIfPlayable)
{
    typedef AnimationData* (__thiscall *GetAnimation)(AnimationController*);
    if (!process || !process->GetState()) return;
{
    AnimationData* a = process->GetState();
    AnimationData* b = a ? a->FUN_0044ddc0() : 0;
    if (b && b->animations.FUN_00474a40()) {
    { AnimationHandle* h;
    { bool i;
    { int f;
    { int j;
    { bool g;
    { AnimationCursor* c;
    { AnimationLink* d;
    { void* e;
    { int k;
    c = b->animations.FUN_00474a40()->FUN_00500940();
    j = b->FUN_00525980(DAT_011dea3c);
    f = 0;
    i = false;
    g = false;
    h = 0;
    if (j && c) {
        int activeCopy = j;
        if (!c->FUN_005f65d0(&activeCopy)) {
            typedef void (__thiscall *Reset)(AnimationController*, int);
            if (process)
                process->SetLink(0);
            j = 0;
        }
    }
    h = (AnimationHandle*)FUN_00576260(j, 0);
    if (skipIfPlayable && j && h &&
        h->FUN_00726070() > 0)
    {
        AnimationHandle* releaseEarly = h;
        AnimationHandle* deleteEarly = releaseEarly;
        deleteEarly ? deleteEarly->FUN_004459e0(1) : 0;
        return;
    }
    {
    AnimationHandle* releasedMid = h;
    AnimationHandle* disposedMid = releasedMid;
    disposedMid ? disposedMid->FUN_004459e0(1) : 0;
    }
    h = 0;
    while (c && *c->FUN_006815c0()) {
        f = *c->FUN_006815c0();
        c = c->FUN_00726070();
        if (j == f) {
            if (g)
                break;
            g = true;
        } else if (g || !j) {
            h = (AnimationHandle*)FUN_00576260(f, 0);
            if (h && h->FUN_00726070() > 0) {
                i = true;
                break;
            }
        }
        if (!c || !*c->FUN_006815c0())
            c = b->animations.FUN_00474a40()->FUN_00500940();
    }
    if (i) {
        if (a->FUN_004bd7a0() >= 0)
            FUN_004bfb70(a->FUN_004bd7a0(), f);
        e = FUN_004bf220(this);
        k = ((ActorAnimation*)e)->FUN_004c8f30(f);
        d = new AnimationLink(f, k);
        typedef void (__thiscall *SetLink)(AnimationController*, AnimationLink*);
        typedef AnimationData* (__thiscall *Toggle)(AnimationController*, int);
        process->SetLink(d);
        process->Toggle(0)->FUN_006ecd40();
        ApplyAnimation(process->GetState()->FUN_0044ddc0(),
            (allowTransition && FUN_008a16d0()) ? 2 : 0,
            ((AnimationHandle*)process->GetState())->FUN_004bda70(), 2, !allowTransition);
    }
    delete h;
}
}
}
}
}
}
}
}
}
}
}
}
