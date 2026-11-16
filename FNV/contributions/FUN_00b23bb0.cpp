struct AllocationException {
    unsigned int vtable;
    unsigned int reserved1;
    unsigned int reserved2;
    void __thiscall FUN_00ec78f1(unsigned int* value);
};
extern unsigned int DAT_010176f8;
extern unsigned int DAT_01140ef8;
void __stdcall FUN_00ec7894(void* exception, void* info);
void* __cdecl FUN_00401000(unsigned int bytes);

void* __cdecl FUN_00b23bb0(unsigned int count)
{
    if (count <= 0u)
        count = 0;
    else if (0xffffffffu / count < 12) {
        unsigned int empty = 0;
        AllocationException exception;
        exception.FUN_00ec78f1(&empty);
        exception.vtable = (unsigned int)&DAT_010176f8;
        FUN_00ec7894(&exception, &DAT_01140ef8);
    }
    return FUN_00401000(count * 12);
}
