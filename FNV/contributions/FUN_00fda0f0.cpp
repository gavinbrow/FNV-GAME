// @fnv 0x00fda0f0
struct S009ff340_Base04 {
    void FUN_004ed900();
    ~S009ff340_Base04() {}
};
struct XL : public S009ff340_Base04 {
    int a, b, c, d, e;
    ~XL() {
        int cleanup_frame[5];
        FUN_004ed900();
    }
};
XL DAT_011f3324;