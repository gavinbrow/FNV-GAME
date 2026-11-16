extern __declspec(thread) int tlsMode;
struct ShortPair { int first; int second; };
struct ByteFlag { unsigned char value; ByteFlag(bool v) : value(v) {} ByteFlag(const ByteFlag &other) : value(other.value) {} };
struct FUN_00c90510_class {
    virtual void vf00();
    virtual void vf04();
    virtual void vf08();
    virtual void vf0c();
    virtual void vf10();
    virtual void vf14();
    virtual void vf18();
    virtual void vf1c();
    virtual void vf20();
    virtual void vf24(ByteFlag flag, ShortPair* output);
    void FUN_00c90510();
    void FUN_00c905b0();
};
struct FUN_00cc49b0_class;
struct FUN_00d21ce0_class {
    int unk0c, unk10, unk14;
    void FUN_00d21ce0(FUN_00cc49b0_class* parent);
};
struct FUN_00cc49b0_class {
    int unk00, unk04, unk08;
    FUN_00d21ce0_class subobject;
    FUN_00c90510_class* owner;
    unsigned short state;
    unsigned short substate;
    void FUN_00cc49b0(FUN_00c90510_class* value);
};
struct ScopedThreadState {
    int previous;
    ScopedThreadState() { previous = tlsMode; tlsMode = 16; }
    ~ScopedThreadState() { tlsMode = previous; }
};
void FUN_00cc49b0_class::FUN_00cc49b0(FUN_00c90510_class* value) {
    ScopedThreadState thread;
    if (value) value->FUN_00c90510();
    if (owner) owner->FUN_00c905b0();
    owner = value;
    ShortPair result;
    owner->vf24(ByteFlag(true), &result);
    state = (unsigned short)result.first;
    substate = (unsigned short)result.second;
    subobject.FUN_00d21ce0(this);
}