struct FUN_006815c0 {
    int unk00;
    FUN_006815c0();
    FUN_006815c0(const FUN_006815c0&);
};
struct FUN_0065d3a0 {
    FUN_0065d3a0(FUN_006815c0 value);
    ~FUN_0065d3a0();
};
struct FUN_0065ca90 : FUN_0065d3a0 {
    FUN_0065ca90();
    void __thiscall FUN_0065d4e0(int value);
};
FUN_0065ca90::FUN_0065ca90() : FUN_0065d3a0(FUN_006815c0()) {
    FUN_0065d4e0(0);
}
