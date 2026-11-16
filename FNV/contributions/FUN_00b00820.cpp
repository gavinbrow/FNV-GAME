struct FUN_00b00820_tail {
    unsigned int pendingState;
    unsigned int otherState;
    unsigned __int64 sequence;
};
struct FUN_00b00820_shell {
    FUN_00b00820_shell* FUN_00b00820(unsigned int value);
    void FUN_00b006b0(unsigned int value);
};

FUN_00b00820_shell* FUN_00b00820_shell::FUN_00b00820(unsigned int value)
{
    reinterpret_cast<FUN_00b00820_tail*>(
        reinterpret_cast<char*>(this) + 0x248)->pendingState = 0;
    reinterpret_cast<FUN_00b00820_tail*>(
        reinterpret_cast<char*>(this) + 0x248)->sequence = 0;
    FUN_00b006b0(value);
    return this;
}