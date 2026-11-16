extern char DAT_0104e1dc;
struct FUN_0062a220 {
    void* vtable;
    FUN_0062a220();
    ~FUN_0062a220();
    void FUN_0062a3b0(unsigned int first, unsigned int second);
};
struct FUN_008c71b0_Class {
    void FUN_008c71b0(int value);
};
struct FUN_009a7bc0 : FUN_0062a220 {
    FUN_009a7bc0(unsigned int first, unsigned int second);
};
FUN_009a7bc0::FUN_009a7bc0(unsigned int first, unsigned int second) {
    vtable = &DAT_0104e1dc;
    reinterpret_cast<FUN_008c71b0_Class*>(reinterpret_cast<char*>(this) + 0x70)->FUN_008c71b0(0);
    FUN_0062a3b0(first, second);
}