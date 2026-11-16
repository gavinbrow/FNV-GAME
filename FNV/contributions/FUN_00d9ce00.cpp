struct FUN_00d9ce00_Class
{
    int base;
    int value;
    int unk08;
    int* items;
    int count;
    int FUN_00d9c450(int start, int first, int second);
    int* FUN_00d9ce00(int first, int second, int* output);
};

int* FUN_00d9ce00_Class::FUN_00d9ce00(int first, int second, int* output)
{
    if (count == 0)
        FUN_00d9c450(value + 0x80, first, second);
    *output = items[count - 1];
    --count;
    return (int*)(((*output * 3) << 4) + base);
}
