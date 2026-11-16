struct Owner {
    virtual void unk00();
    virtual void unk04();
    virtual void unk08();
    virtual void unk0c();
    virtual void unk10();
    virtual void unk14();
    virtual void forward(unsigned int, unsigned int, unsigned int,
                        float, float, float, unsigned int);
};
struct Interface {
    void FUN_00ddc9c0(unsigned int, unsigned int, unsigned int,
                      float, float, float, unsigned int);
};
void Interface::FUN_00ddc9c0(unsigned int a, unsigned int b, unsigned int c,
                              float d, float e, float f, unsigned int g) {
    Owner* owner = *(Owner**)((char*)this - 8);
    owner->forward(a, b, c, d, e, f, g);
}
