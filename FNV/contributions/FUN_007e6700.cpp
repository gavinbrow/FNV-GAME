struct FUN_007e6700_Helper
{
    void* __thiscall FUN_007170a0(int);
    void* __thiscall FUN_00458b50();
};

struct FUN_007e6700_Object28
{
    void __thiscall FUN_00a01350(int, void*);
};

struct FUN_007e6700_Object2C
{
    void __thiscall FUN_00700320(int, bool);
};

typedef bool (__cdecl *FUN_007e6700_Callback)(void*);

struct FUN_007e6700_Class
{
    char padding00[0x28];
    FUN_007e6700_Object28* object28;
    FUN_007e6700_Object2C* object2C;
    char padding30[4];
    FUN_007e6700_Helper helper;
    char padding38[0x58 - 0x38];
    FUN_007e6700_Callback callback;

    void __thiscall FUN_007e6700();
};

void __thiscall FUN_007e6700_Class::FUN_007e6700()
{
    object28->FUN_00a01350(0xFC4, helper.FUN_007170a0(1));

    if (callback != 0)
    {
        object2C->FUN_00700320(0xFAF, callback(helper.FUN_00458b50()));
    }
}