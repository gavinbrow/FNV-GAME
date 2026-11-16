struct Container { int FUN_00c918e0(void* value); };
struct Owner { int FUN_00d6a910(Container* container); };
int Owner::FUN_00d6a910(Container* container)
{
    void* value;
    if ((char*)this - 0x20) value = (char*)this + 8;
    else value = 0;
    return container->FUN_00c918e0(value);
}
