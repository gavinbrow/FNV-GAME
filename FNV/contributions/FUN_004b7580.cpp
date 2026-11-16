namespace fnv_00a16ea0
{
    void FUN_00ec7c66(char* destination, int destinationSize, const char* source, int count);
}

// @fnv 0x004b7580
void FUN_004b7580(char* destination, int destinationSize, const char* source, int count)
{
    fnv_00a16ea0::FUN_00ec7c66(destination, destinationSize, source, count);
}
