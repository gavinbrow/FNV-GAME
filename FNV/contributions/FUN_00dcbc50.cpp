struct FUN_00dcbc50_Item {
    int unk00;
    int unk04;
    __int64 value;
};

struct FUN_00dcbc50_Argument {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int count;
};

struct FUN_00dcbc50_Result {
    FUN_00dcbc50_Argument* entry;
    int index;
};

struct FUN_00dcbc50_Class {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00dcbc50_Item* items;

    void FUN_00dcba40(FUN_00dcbc50_Result* result, FUN_00dcbc50_Argument* argument, int mode);
    __int64 FUN_00dcbc50(FUN_00dcbc50_Argument* argument);
};

__int64 FUN_00dcbc50_Class::FUN_00dcbc50(FUN_00dcbc50_Argument* argument)
{
    FUN_00dcbc50_Result result;
    FUN_00dcba40(&result, argument, 0);

    if ((unsigned int)(result.entry->count - 1) <= 1)
        return items[result.index].value;

    return 0;
}