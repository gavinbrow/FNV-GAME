struct BoundingBlock {
    FUN_00b02c10_class contained;
    int extra38;
    __forceinline ~BoundingBlock() { contained.FUN_00b02c10(); }
};
struct BranchBlock {
    FUN_00b02d40_class contained;
    __forceinline ~BranchBlock() { contained.FUN_00b02d40(); }
};
struct LeafBlock {
    FUN_00b02e00_class contained;
    int extra04,extra08,extra0c,extra10;
    __forceinline ~LeafBlock() { contained.FUN_00b02e00(); }
};
struct FUN_00b02ac0 {
    BoundingBlock root;
    BoundingBlock bounds;
    BranchBlock limbA;
    BranchBlock limbB;
    LeafBlock leafA;
    LeafBlock leafB;
    LeafBlock leafC;
    ~FUN_00b02ac0();
};
FUN_00b02ac0::~FUN_00b02ac0() {}
