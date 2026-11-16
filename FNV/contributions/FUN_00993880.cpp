extern int DAT_0108db4c;

void __cdecl FUN_004ede70(void*);

struct FUN_00991130_class
{
    void __thiscall FUN_00993880();
    void __thiscall FUN_00991130();
};

void __thiscall FUN_00991130_class::FUN_00993880()
{
    *(int*)this = (int)&DAT_0108db4c;
    FUN_004ede70(*(void**)((char*)this + 4));
}