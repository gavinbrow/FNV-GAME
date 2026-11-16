struct FUN_00e89410_Class
{
    void* __thiscall FUN_00e89250(unsigned int index);
    void* __thiscall FUN_00e892d0(unsigned int index);
    void* __thiscall FUN_00e89410(unsigned int index);
};

extern unsigned int DAT_011bf558;

void* __thiscall FUN_00e89410_Class::FUN_00e89410(unsigned int index)
{
    void* item = 0;

    if (index < DAT_011bf558)
        item = FUN_00e89250(index);

    void* result = FUN_00e892d0(index);

    if (item)
        result = item;

    return result;
}