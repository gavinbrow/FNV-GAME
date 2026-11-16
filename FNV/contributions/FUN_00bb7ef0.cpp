void* __cdecl FUN_00aa13e0(unsigned int);
class FUN_00bb7c30_Class {
public:
    static void* operator new(unsigned int) { return FUN_00aa13e0(0xb0); }
    FUN_00bb7c30_Class(int flag);
};
FUN_00bb7c30_Class* __cdecl FUN_00bb7ef0()
{
    return new FUN_00bb7c30_Class(0);
}