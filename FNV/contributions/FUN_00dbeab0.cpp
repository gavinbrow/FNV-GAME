struct ObjectHandle
{
    void* object;
    __declspec(nothrow) int FUN_00dbac00();
    __declspec(nothrow) void FUN_00dbab70();
    ~ObjectHandle() { FUN_00dbab70(); }
};
struct StringHandle
{
    void* object;
    __declspec(nothrow) int FUN_00dba980();
    __declspec(nothrow) void FUN_00dba7f0();
    ~StringHandle() { FUN_00dba7f0(); }
};
struct Value
{
    int FUN_00dbac40();
    int FUN_00dbac90();
    float FUN_00dbac80();
    void* FUN_00dbac70();
    __declspec(nothrow) ObjectHandle FUN_00dbacd0();
    __declspec(nothrow) StringHandle FUN_00dbaca0();
};
int __stdcall FUN_00dbeab0(Value* value)
{
    if(value->FUN_00dbac40() >= 16)
        return value->FUN_00dbacd0().FUN_00dbac00();
    switch(value->FUN_00dbac40())
    {
    case 0: return 0;
    case 1: case 2: return value->FUN_00dbac90() != 0;
    case 3: return value->FUN_00dbac80() != 0.0f;
    case 4: case 6: case 7: return 1;
    case 8: case 9: return value->FUN_00dbaca0().FUN_00dba980() == 0;
    case 16: return value->FUN_00dbacd0().FUN_00dbac00() != 0;
    case 10: return value->FUN_00dbac70() != 0;
    default: return 0;
    }
}

