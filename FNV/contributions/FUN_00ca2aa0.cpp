struct Allocator { void FUN_00aa4060(void* p); };
extern Allocator DAT_011f6238;
struct Special {
    void FUN_00ca2140();
    Special* FUN_00ca2aa0(unsigned int flags);
};
Special* Special::FUN_00ca2aa0(unsigned int flags) {
    FUN_00ca2140();
    if ((flags & 1) && this) {
        unsigned char shift = *((unsigned char*)this - 1);
        DAT_011f6238.FUN_00aa4060((char*)this - shift);
    }
    return this;
}
