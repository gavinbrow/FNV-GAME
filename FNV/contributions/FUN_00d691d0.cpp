struct Heap {
    virtual void a();
    virtual void b();
    virtual void free(void*, unsigned short);
};
struct Holder { int unk00; int unk04; int unk08; int unk0C; Heap* unk10; };
struct Destructor { void FUN_00d690d0(); };
struct FUN_00d691d0_Class {
    int unk00;
    unsigned short allocationSize;
    unsigned short unk06;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    FUN_00d691d0_Class* FUN_00d691d0(unsigned int flags);
};
extern Holder* FUN_00c85750();
FUN_00d691d0_Class* FUN_00d691d0_Class::FUN_00d691d0(unsigned int flags) {
    ((Destructor*)this)->FUN_00d690d0();
    if (flags & 1) {
        Holder* holder = FUN_00c85750();
        holder->unk10->free(this, allocationSize);
    }
    return this;
}
