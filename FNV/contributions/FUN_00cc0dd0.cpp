struct CallbackInterface {
    virtual void reserved0();
    virtual void reserved1();
    virtual void notify(void*, unsigned short);
};
struct State {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    CallbackInterface* interface10;
};
State* __cdecl FUN_00c85750();
struct Object {
    void* unk00;
    unsigned short unk04;
    void FUN_00cc0ae0();
    Object* FUN_00cc0dd0(unsigned int flags);
};
Object* Object::FUN_00cc0dd0(unsigned int flags) {
    FUN_00cc0ae0();
    if (flags & 1) {
        State* state = FUN_00c85750();
        state->interface10->notify(this, unk04);
    }
    return this;
}
