struct FUN_008c71b0 {
    unsigned int value;
    FUN_008c71b0(unsigned int v);
    FUN_008c71b0(const FUN_008c71b0& other);
};

struct LoadBuffer4160 {
    virtual void Slot0();
    virtual int GetVersion();
    void FUN_00428110(unsigned int* out);
    void FUN_0042ce30(unsigned int* out);
    void FUN_007037c0(int version);
    void FUN_00428130(FUN_008c71b0 flags);
    void FUN_00428130(unsigned int flags);
    void FUN_0086cf00(FUN_008c71b0 flags);
    void FUN_0086cf00(unsigned int flags);
    unsigned int FUN_00864a60();
};

struct Item4160 : FUN_0076b630 {
    void FUN_004bee00(LoadBuffer4160* buffer);
    void FUN_004bc780();
};

struct ChangeList4160 {
    void FUN_005ae3d0(FUN_004459e0** item);
};

struct Inventory4160 {
    ChangeList4160* changes;
    void FUN_004d4160(LoadBuffer4160* buffer);
};

void Inventory4160::FUN_004d4160(LoadBuffer4160* buffer)
{
    int tag = buffer->GetVersion();
    unsigned int oldFlags;
    buffer->FUN_00428110(&oldFlags);
    unsigned int savedMode;
    buffer->FUN_0042ce30(&savedMode);
    buffer->FUN_007037c0(0);
    buffer->FUN_00428130(FUN_008c71b0(0x400));
    buffer->FUN_0086cf00(FUN_008c71b0(0));
    unsigned int itemCount = buffer->FUN_00864a60();
    for (unsigned int i = 0; i < itemCount; i++) {
        FUN_004459e0* item = new FUN_0076b630;
        static_cast<Item4160*>(item)->FUN_004bee00(buffer);
        if (!static_cast<Item4160*>(item)->FUN_0044ddc0()) {
            static_cast<Item4160*>(item)->FUN_004bc780();
            delete item;
            item = 0;
        }
        changes->FUN_005ae3d0(&item);
    }
    buffer->FUN_007037c0(tag);
    buffer->FUN_00428130(oldFlags);
    buffer->FUN_0086cf00(savedMode);
}
