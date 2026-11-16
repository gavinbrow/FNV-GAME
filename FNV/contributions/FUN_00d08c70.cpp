struct FUN_00d9a4d0_class {
    void __thiscall FUN_00d9a4d0(unsigned int value);
};
struct FUN_00d08c70_class {
    int unk00;
    int unk04;
    int unk08;
    FUN_00d9a4d0_class* unk0C;
    void __thiscall FUN_00d08c70(void* arg);
};
void FUN_00d08c70_class::FUN_00d08c70(void* arg)
{
    typedef unsigned short (__stdcall *FunctionReturningWord)(void*);
    unsigned int value = ((FunctionReturningWord)&FUN_00d083e0)(arg);
    ((FUN_00d9a4d0_class*)((char*)unk0C + 0x1c))->FUN_00d9a4d0(value);
}
