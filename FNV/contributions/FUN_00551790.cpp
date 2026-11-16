struct CellLabel : VCallC8 {
    virtual void v51(); virtual void v52(); virtual void v53();
    virtual void v54(); virtual void v55(); virtual void v56();
    virtual void v57(); virtual void v58(); virtual void v59();
    virtual void v60(); virtual void v61(); virtual void v62();
    virtual void v63(); virtual void v64(); virtual void v65();
    virtual void v66(); virtual void v67(); virtual void v68();
    virtual void v69(); virtual void v70(); virtual void v71();
    virtual void v72(); virtual void v73(); virtual void v74();
    virtual void v75();
    virtual unsigned int v76();

    bool FUN_00425fd0();
    CellLabel* FUN_0054ddd0();
    int FUN_00544c60();
    int FUN_00544c30();
    void FUN_00551790(char* destination);
};

extern void __cdecl FUN_00406f60(char* destination, const char* format, ...);
extern const char DAT_0102f0d8[];
extern const char DAT_0102f0a8[];
extern const char DAT_0102f088[];

void CellLabel::FUN_00551790(char* destination) {
    if (FUN_00425fd0()) {
        FUN_00406f60(destination, DAT_0102f0d8, v76(), _ref_0084e3a0(this));
    } else {
        CellLabel* worldSpace = FUN_0054ddd0();
        if (worldSpace) {
            FUN_00406f60(destination, DAT_0102f0a8, v76(), _ref_0084e3a0(this),
                          FUN_00544c30(), FUN_00544c60(),
                          worldSpace->v76(), _ref_0084e3a0(worldSpace));
        } else {
            FUN_00406f60(destination, DAT_0102f088, v76(), _ref_0084e3a0(this),
                          FUN_00544c30(), FUN_00544c60());
        }
    }
}