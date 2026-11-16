struct Allocator { virtual void slot0(); virtual void slot1(); virtual void Free(void* object, unsigned short size); };
struct Holder { unsigned int unk00; unsigned int unk04; unsigned int unk08; unsigned int unk0c; Allocator* allocator; };
Holder* FUN_00c85750();
struct hkaAnimationPreviewColorContainer {
    unsigned int unk00;
    unsigned short allocationSize;
    hkaAnimationPreviewColorContainer* FUN_00dfe6b0(unsigned int flags);
    void FUN_00e41e20();
};
hkaAnimationPreviewColorContainer* hkaAnimationPreviewColorContainer::FUN_00dfe6b0(unsigned int flags) {
    FUN_00e41e20();
    if (flags & 1) { Holder* holder = FUN_00c85750(); Allocator* allocator = holder->allocator; unsigned short size = allocationSize; allocator->Free(this, size); }
    return this;
}

