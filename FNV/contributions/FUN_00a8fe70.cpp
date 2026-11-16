
extern const void* DAT_0109f7f4;
extern unsigned int DAT_011f5e48;
struct FNVObj {
    const void* vft;
    unsigned int references;
    ReferenceHandle handle;
    FNVObj* FUN_00a8fe70(const ReferenceHandle& src);
};
FNVObj* FNVObj::FUN_00a8fe70(const ReferenceHandle& src) {
    vft = &vftable_NiRefObject;
    references = 0;
    InterlockedIncrement(&DAT_011f4400);
    vft = &DAT_0109f7f4;
    handle.value = (volatile long*)DAT_0109b220;
    handle = src;
    unsigned int capacity = DAT_011f5e48;
    if (DAT_011f5e4c == capacity) {
        if (capacity > 0)
            capacity += capacity;
        else
            capacity = 1;
        ((NiStreamLinkIDSet*)&DAT_011f5e44)->Realloc(capacity);
    }
    ((FNVObj**)DAT_011f5e44)[DAT_011f5e4c] = this;
    ++DAT_011f5e4c;
    return this;
}
