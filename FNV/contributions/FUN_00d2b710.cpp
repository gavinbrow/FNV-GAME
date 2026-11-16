struct ManagerVTable {
    virtual void unused0();
    virtual void unused1();
    virtual void notify(void* object, unsigned short value);
};
struct AudioState {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    ManagerVTable* unk10;
};
struct Base {
    void FUN_00d2b6b0();
};
struct Widget : Base {
    int unk00;
    unsigned short unk04;
    int unk06;
    void* FUN_00d2b710(unsigned char flags);
};
extern AudioState* __cdecl FUN_00c85750();
void* Widget::FUN_00d2b710(unsigned char flags)
{
    FUN_00d2b6b0();
    if (flags & 1)
    {
        AudioState* state = FUN_00c85750();
        state->unk10->notify(this, unk04);
    }
    return this;
}
