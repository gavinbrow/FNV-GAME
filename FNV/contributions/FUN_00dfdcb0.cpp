struct Ref { void removeReference(); };
struct Heap {
    virtual void a();
    virtual void b();
    virtual void free(void*, unsigned short);
};
struct Holder { int unk00; int unk04; int unk08; int unk0C; Heap* unk10; };
struct Helper { void FUN_00dfdb90(); };
struct Owner {
    int unk00;
    unsigned short unk04;
    unsigned short unk06;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    Ref* unk20;
    Owner* FUN_00dfdcb0(unsigned int flags);
};
extern Holder* FUN_00c85750();
Owner* Owner::FUN_00dfdcb0(unsigned int flags) {
    if (unk20) unk20->removeReference();
    unk20 = 0;
    ((Helper*)this)->FUN_00dfdb90();
    if (flags & 1) {
        Holder* holder = FUN_00c85750();
        holder->unk10->free(this, unk04);
    }
    return this;
}
