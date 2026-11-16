struct TileValue { float __thiscall FUN_00a011b0(int trait); };
struct ListNode {
    bool __thiscall FUN_008256d0();
    ListNode* __thiscall FUN_00726070();
    TileValue*** __thiscall FUN_006815c0();
};
struct ListOwner {
    int ownerData;
    ListNode firstNode;
    int* __thiscall FUN_007a6fa0(unsigned int requested, unsigned char byIndex);
};
int* ListOwner::FUN_007a6fa0(unsigned int requested, unsigned char byIndex) {
    if (firstNode.FUN_008256d0()) return 0;
    ListNode* node = this ? &firstNode : 0;
    if (byIndex) {
        unsigned int index = 0;
        while (node != 0 && index++ != requested)
            node = node->FUN_00726070();
    } else {
        while (node != 0 && (**node->FUN_006815c0())->FUN_00a011b0(0xfac) != requested)
            node = node->FUN_00726070();
    }
    return node ? (int*)*node->FUN_006815c0() : 0;
}