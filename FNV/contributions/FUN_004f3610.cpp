struct ActionItem {
    virtual void V0();
    virtual void V1();
    virtual void V2();
    virtual void V3();
    virtual void V4();
    virtual void V5();
    virtual void V6();
    virtual void V7();
    virtual bool CheckState();
};
struct ActionIterator {
    ActionItem** FUN_006815c0();
    bool FUN_004f3610();
};
bool ActionIterator::FUN_004f3610() {
    ActionIterator* current = this;
    while (current != 0 && *current->FUN_006815c0() != 0) {
        if (!(*current->FUN_006815c0())->CheckState())
            return false;
    }
    return true;
}