// FUN_006f6250: __thiscall (this in ecx), callee pops 4 bytes (1 stack parameter)
struct FUN_006e5cc0_shell
{
    void __thiscall FUN_006e5cc0(void* apObject);
};

struct FUN_006f6250_shell
{
    void FUN_006f6250(FUN_006e5cc0_shell* apObject);
};

void FUN_006f6250_shell::FUN_006f6250(FUN_006e5cc0_shell* apObject)
{
    apObject->FUN_006e5cc0((void*)((char*)this + 0x4c));
}
