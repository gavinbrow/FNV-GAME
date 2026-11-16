struct FUN_00ba3840_Class {
    void __thiscall FUN_00ba3840(int value);
};
struct FUN_00ba3aa0_Class {
    void __thiscall FUN_00ba3aa0(int kind, void* value);
};
struct FUN_00ba37f0_Class {
    void __thiscall FUN_00ba37f0(int value);
};
int __cdecl FUN_00b54090();
struct FUN_00b5a340_Class {
    void __thiscall FUN_00b5a340(int arg);
};
void FUN_00b5a340_Class::FUN_00b5a340(int arg)
{
    char* value;
    FUN_00ba37f0_Class* object;
    value = (char*)this + 0xb4;
    ((FUN_00ba3840_Class*)value)->FUN_00ba3840(0x28);
    ((FUN_00ba3aa0_Class*)((char*)this + 0x28))->FUN_00ba3aa0(2, &value);
    object = (FUN_00ba37f0_Class*)((char*)this + 0xc4);
    value = (char*)object;
    object->FUN_00ba37f0(FUN_00b54090());
    ((FUN_00ba3aa0_Class*)((char*)this + 0x28))->FUN_00ba3aa0(3, &value);
}