struct Callback {
    virtual void unk00();
    virtual void unk04();
    virtual void update(void* entries, int bytes);
};
struct FUN_00dc3b60_class {
    void** entries;
    unsigned int flags;
    int count;
    void __thiscall FUN_00dc38f0();
    void __thiscall FUN_00dc3b60(Callback* callback);
};
void FUN_00dc3b60_class::FUN_00dc3b60(Callback* callback) {
    FUN_00dc38f0();
    if ((flags & 0x80000000) == 0)
        callback->update(entries, (count + 1) * 12);
}
