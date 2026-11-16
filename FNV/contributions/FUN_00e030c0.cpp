int __cdecl FUN_00e030c0(int index, int* data)
{
    int base = *data;
    *data = base + 4;
    return *(int*)(base + index);
}