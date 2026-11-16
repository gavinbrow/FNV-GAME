struct FUN_00594cd0_Entry
{
    int field00;
    int field04;
    int field08;
    int field0c;
};

struct FUN_00594cd0_Class
{
    FUN_00594cd0_Entry entries[32];
    unsigned int count;

    FUN_00594cd0_Entry* __thiscall FUN_00594cd0(FUN_00594cd0_Entry* result);
};

FUN_00594cd0_Entry* __thiscall
FUN_00594cd0_Class::FUN_00594cd0(FUN_00594cd0_Entry* result)
{
    *result = entries[count];
    count = count - 1;
    return result;
}