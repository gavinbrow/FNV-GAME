struct FUN_006f4b10 : FUN_006f4b40 { FUN_006f4b10(); };
struct FUN_006f4b60 : FUN_006f4b90 { FUN_006f4b60(); };
struct FUN_006815c0 { int unk00; int unk04; int unk08; FUN_006815c0(); };
struct FUN_006f48b0 {
    FUN_006f4b10 first;
    FUN_006f4b60 second;
    FUN_006815c0 third;
    FUN_006815c0 fourth;
    FUN_006f48b0();
};
FUN_006f48b0::FUN_006f48b0()
    : first(), second(), third(), fourth() {}