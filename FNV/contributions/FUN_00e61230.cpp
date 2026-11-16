struct FUN_00e61230_Buffer {
    unsigned int field00;
    unsigned int field04;
    unsigned int field08;
    unsigned int field0c;
    unsigned int field10;
    unsigned int field14;
    unsigned int field18;
    unsigned int field1c;
    unsigned int field20;
    unsigned int field24;
};
struct FUN_00e61230_Receiver {
    virtual void unknown0() = 0;
    virtual void unknown1() = 0;
    virtual void unknown2() = 0;
    virtual void unknown3() = 0;
    virtual void begin(void* value, unsigned int mode, FUN_00e61230_Buffer* buffer) = 0;
    virtual void end(FUN_00e61230_Buffer* buffer) = 0;
};
extern "C" void __cdecl FUN_00e611d0(FUN_00e61230_Buffer* buffer, unsigned int stage);
void __cdecl FUN_00e61230(FUN_00e61230_Receiver* receiver, void* value, unsigned int stage) {
    FUN_00e61230_Buffer buffer;
    receiver->begin(value, 1, &buffer);
    FUN_00e611d0(&buffer, stage);
    receiver->end(&buffer);
}