struct FUN_00d87430_Class
{
    int __thiscall FUN_00d87430(int index);
};
struct FUN_00d47970_Class
{
    int unk00;
    int unk04;
    FUN_00d874d0_s m_map08;

    void FUN_00d47970(void* iterator);
};

void FUN_00d47970_Class::FUN_00d47970(void* iterator)
{
    FUN_00d87410_Class* registry =
        (FUN_00d87410_Class*)((char*)iterator + 8);
    int index = registry->FUN_00d87410();
    ((FUN_00d874b0_class*)registry)->FUN_00d874b0((char*)&iterator, index);
    if (*(char*)&iterator != 0)
    {
        FUN_00d874d0_s* destination = &m_map08;
        do
        {
            int key = ((FUN_00d87440_Class*)registry)->FUN_00d87440(index);
            int value = ((FUN_00d87430_Class*)registry)->FUN_00d87430(index);
            destination->FUN_00d874d0((const char*)value, key);
            index = ((hkCachedHashMap*)registry)->FUN_00d87480(index);
            ((FUN_00d874b0_class*)registry)->FUN_00d874b0((char*)&iterator, index);
        } while (*(char*)&iterator != 0);
    }
}