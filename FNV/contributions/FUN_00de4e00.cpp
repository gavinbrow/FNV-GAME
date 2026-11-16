struct CpuObject { char* FUN_00de4e00(); };
char* CpuObject::FUN_00de4e00()
{
    return reinterpret_cast<char*>(this) + 128;
}
