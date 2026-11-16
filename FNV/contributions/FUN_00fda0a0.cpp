struct A { ~A() {} };
struct TileList : A {
    void FUN_004ed900();
    ~TileList() { char pad[16]; FUN_004ed900(); }
};
TileList DAT_011f3318;
