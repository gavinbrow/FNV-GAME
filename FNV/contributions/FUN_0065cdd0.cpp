struct FUN_006815c0 { int value; FUN_006815c0(); FUN_006815c0(const FUN_006815c0&); };
struct FUN_0065d3a0 {
    FUN_0065d3a0(FUN_006815c0 value);
    ~FUN_0065d3a0();
    void __thiscall FUN_0065d980(int value);
};
struct FUN_0065cdd0 : FUN_0065d3a0 { FUN_0065cdd0(); };
FUN_0065cdd0::FUN_0065cdd0() : FUN_0065d3a0(FUN_006815c0()) { FUN_0065d980(0); }