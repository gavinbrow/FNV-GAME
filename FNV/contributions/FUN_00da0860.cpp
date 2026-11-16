struct FUN_00df67d0_Base {
    virtual void v0();
    void FUN_00df67d0();
};
struct FUN_00da0860_manager {
    virtual void v0();
    virtual void v1();
    virtual void FUN_00da0860_release(void *, unsigned short);
};
struct BSAudio { int unk00; int unk04; int unk08; int unk0C; FUN_00da0860_manager *unk10; };
BSAudio *FUN_00c85750();
struct FUN_00da0860_class : FUN_00df67d0_Base {
    unsigned short unk04;
    FUN_00da0860_class *FUN_00da0860(unsigned int flags);
};
FUN_00da0860_class *FUN_00da0860_class::FUN_00da0860(unsigned int flags) {
    FUN_00df67d0_Base::FUN_00df67d0();
    if (flags & 1) {
        BSAudio *audio = FUN_00c85750();
        audio->unk10->FUN_00da0860_release(this, unk04);
    }
    return this;
}
