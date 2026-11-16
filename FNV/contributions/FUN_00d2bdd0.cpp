struct ReaderWithPosition {
    virtual void Slot00() = 0;
    virtual void Slot01() = 0;
    virtual void Slot02() = 0;
    virtual void Slot03() = 0;
    virtual void Slot04() = 0;
    virtual void Slot05() = 0;
    virtual void Slot06() = 0;
    virtual void Slot07() = 0;
    virtual void Slot08() = 0;
    virtual void Slot09() = 0;
    virtual void Slot10() = 0;
    virtual int GetPosition() = 0;
    int unk04;
    int position;
    int FUN_00d2bdd0(int unused);
};
int ReaderWithPosition::FUN_00d2bdd0(int unused) {
    int value = GetPosition();
    int failed = value == -1;
    position = value;
    return failed;
}
