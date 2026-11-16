struct CpuObject { int* values; int* FUN_00d87230(int index); };
int* CpuObject::FUN_00d87230(int index)
{
    return values + index;
}
