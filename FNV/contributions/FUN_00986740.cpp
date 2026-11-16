struct BSSimpleArrayForCall : BSSimpleArray
{
    void __thiscall FUN_0098f580(BSSimpleArrayForCall* other);
};

struct FUN_00986740_shell
{
    void* unk00;
    void* unk04;
    BSSimpleArrayForCall arr;

    void __thiscall FUN_00986740(FUN_00986740_shell* other);
};

void __thiscall BSSimpleArrayForCall::FUN_0098f580(BSSimpleArrayForCall* other)
{
}

void __thiscall FUN_00986740_shell::FUN_00986740(FUN_00986740_shell* other)
{
    other->arr.FUN_0098f580(&arr);
}