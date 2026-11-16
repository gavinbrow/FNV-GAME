struct CB1A90Argument {
    virtual void Dummy0();
    virtual void Dummy1();
    virtual void Process(int data, int size);
};
struct CB1A90Owner {
    int data;
    int flags;
    int count;
    void FUN_00cb1a60();
    void FUN_00cb1a90(CB1A90Argument* argument);
};
void CB1A90Owner::FUN_00cb1a90(CB1A90Argument* argument)
{
    FUN_00cb1a60();
    if (!(flags & 0x80000000)) {
        argument->Process(data, (count + 1) << 3);
    }
}