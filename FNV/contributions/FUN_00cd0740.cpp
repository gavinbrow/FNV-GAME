extern const char str_01094d90[];

struct Gap040 {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
};
struct Gap038 {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
};
struct Gap400 {
    Gap040 g00;
    Gap040 g01;
    Gap040 g02;
    Gap040 g03;
    Gap040 g04;
    Gap040 g05;
    Gap040 g06;
    Gap040 g07;
    Gap040 g08;
    Gap040 g09;
    Gap040 g0a;
    Gap040 g0b;
    Gap040 g0c;
    Gap040 g0d;
    Gap040 g0e;
    Gap040 g0f;
};

struct Pair {
    int a;
    int b;
};

struct Flags {
    unsigned int bits;
};

struct Svc {
    virtual void s0();
    virtual int s1(int a, int b);
};

struct Sub0b0c {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c, unk20;
};

struct FUN_00d5e960_t {
    void __thiscall FUN_00d5e960(int v);
};

struct Owner {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3(Sub0b0c* s, const char* g, unsigned int flags);
    Svc* svc;
    Gap400 ga;
    Gap400 gb;
    Gap040 gc00;
    Gap040 gc01;
    Gap040 gc02;
    Gap040 gc03;
    Gap040 gc04;
    Gap040 gc05;
    Gap040 gc06;
    Gap040 gc07;
    Gap040 gc08;
    Gap040 gc09;
    Gap040 gc0a;
    Gap038 gd;
    int f0b00;
    int f0b04;
    int unk0b08;
    Sub0b0c sub0b0c;
    FUN_00d5e960_t cnt0b30;
    Sub0b0c* FUN_00cd0740(const Pair* p, Flags flags);
};

Sub0b0c* Owner::FUN_00cd0740(const Pair* p, Flags flags)
{
    f0b00 = p->a;
    f0b04 = p->b;
    if (flags.bits & 1) {
        v3(&sub0b0c, str_01094d90, flags.bits);
    }
    if (flags.bits & 2) {
        int b = p->b;
        if (b) {
            int r = svc->s1(b, b);
            cnt0b30.FUN_00d5e960(r);
        }
    }
    return &sub0b0c;
}
