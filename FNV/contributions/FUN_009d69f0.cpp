struct FUN_009ca680 {
    virtual ~FUN_009ca680();
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    FUN_009ca680();
};
struct FUN_0097ede0 {
    unsigned int x, y, z, w;
    FUN_0097ede0();
};
struct FUN_00906f60 {
    unsigned int x, y;
    FUN_00906f60();
};
struct FUN_006815c0 {
    unsigned int x, y, z;
    FUN_006815c0();
};
struct FUN_00633c90 {
    unsigned int value;
    FUN_00633c90(int);
    ~FUN_00633c90();
};
struct MoveInput {
    FUN_0097ede0* FUN_006815c0();
    unsigned int FUN_0044edb0();
    bool FUN_0097be60(int);
};
struct FUN_009d69f0 : FUN_009ca680 {
    unsigned int unk10;
    FUN_0097ede0 startTransform;
    FUN_0097ede0 currentTransform;
    float rate;
    unsigned int target38;
    unsigned int mode;
    FUN_00906f60 pos40;
    FUN_006815c0 pos48;
    bool active54;
    FUN_00633c90 state58;
    bool active5C;
    int unk60;
    FUN_00906f60 state64;
    FUN_00906f60 state6C;
    FUN_00906f60 state74;
    FUN_009d69f0(MoveInput* input, float speed, unsigned int flags);
    virtual ~FUN_009d69f0();
};
FUN_009d69f0::FUN_009d69f0(MoveInput* input, float speed, unsigned int flags)
    : unk10(0), startTransform(), currentTransform(), rate(speed),
      target38(0), mode(flags), pos40(), pos48(), active54(false),
      state58(0), active5C(false), unk60(-1),
      state64(), state6C(), state74() {
    if (input) {
        startTransform = *input->FUN_006815c0();
        currentTransform = startTransform;
        target38 = input->FUN_0044edb0();
        if (input->FUN_0097be60(2))
            rate = -rate;
    }
}