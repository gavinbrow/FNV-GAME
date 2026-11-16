extern int DAT_010c6234;
void __cdecl FUN_00aa1460(void* object, unsigned int size);
struct FUN_00c90000_Object {
    int* m_vftable;
    void __thiscall FUN_00c81550();
    FUN_00c90000_Object* __thiscall FUN_00c90000(unsigned int flags);
};
FUN_00c90000_Object* FUN_00c90000_Object::FUN_00c90000(unsigned int flags)
{
    m_vftable = &DAT_010c6234;
    FUN_00c81550();
    if (flags & 1)
        FUN_00aa1460(this, 0x50);
    return this;
}