// @fnv 0x00ec40ec
int __fastcall FUN_00ec40ec(int* item)
{
    char* base = reinterpret_cast<char*>(item);
    int* metadata = *reinterpret_cast<int**>(*item - 4);
    int result = reinterpret_cast<int>(base) - metadata[1];
    int adjustment = metadata[2];
    if (adjustment != 0)
        result -= *reinterpret_cast<int*>(base - adjustment);
    return result;
}