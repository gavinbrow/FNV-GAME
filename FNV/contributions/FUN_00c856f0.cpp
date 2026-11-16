struct Child {
    virtual void unused0(); virtual void unused1(); virtual void unused2(); virtual void unused3();
    virtual void unused4(); virtual void unused5(); virtual void unused6(); virtual void unused7();
    virtual void unused8(); virtual void unused9(); virtual void unused10(); virtual void unused11();
    virtual void Release();
};
struct Owner {
    int unk00, unk04, unk08;
    Child* child0C; Child* child10; Child* child14; Child* child18; Child* child1C;
    void FUN_00c856f0();
};
void Owner::FUN_00c856f0() {
    child14->Release(); child1C->Release(); child10->Release(); child18->Release(); child0C->Release();
}
