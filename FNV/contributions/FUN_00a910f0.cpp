extern const void* DAT_0109f9bc;
void __cdecl FUN_00a47600(void*);
struct FUN_00a910f0_class {
    void* vft;
    void* buffer;
    FUN_00a910f0_class* FUN_00a910f0(unsigned char flags);
};
struct FUN_00aa4060_class {
    void FUN_00aa4060(void* object);
};
extern FUN_00aa4060_class DAT_011f6238;
FUN_00a910f0_class* FUN_00a910f0_class::FUN_00a910f0(unsigned char flags) {
    vft = &DAT_0109f9bc;
    FUN_00a47600(buffer);
    if (flags & 1) DAT_011f6238.FUN_00aa4060(this);
    return this;
}