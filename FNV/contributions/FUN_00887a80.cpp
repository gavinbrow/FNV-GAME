struct FUN_00622570 {
    unsigned int state;
    FUN_00622570(unsigned char flag);
};
struct FUN_00cb8fe0_Class {
    void __thiscall FUN_00cb8fe0(void* context, FUN_00622570 state);
};
struct FUN_00887a80_Class {
    FUN_00cb8fe0_Class* __thiscall FUN_00887a10();
    void* __thiscall FUN_004ae750();
    void __thiscall FUN_00887a80(unsigned char flag);
};
void FUN_00887a80_Class::FUN_00887a80(unsigned char flag)
{
    FUN_00cb8fe0_Class* receiver = FUN_00887a10();
    if (receiver) {
        receiver->FUN_00cb8fe0(FUN_004ae750(), flag);
    }
}
