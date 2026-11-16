struct FUN_00a30c80_shell {
    unsigned __int64 __thiscall FUN_00a30580(void* arg);
    bool __thiscall FUN_00a30c80(void* arg);
};
bool __stdcall FUN_00a30ab0(void* arg);
bool FUN_00a30c80_shell::FUN_00a30c80(void* arg)
{
    if (arg)
    {
        void* linked = *reinterpret_cast<void**>(static_cast<char*>(arg) + 0x58);
        if (linked)
        {
            if (linked == this)
                goto failure;
            unsigned __int64 result = FUN_00a30580(linked);
            if (!static_cast<unsigned char>(result))
                goto failure;
            arg = reinterpret_cast<void*>(static_cast<unsigned int>(result >> 32));
        }
        if (FUN_00a30ab0(arg))
            return true;
    }
failure:
    return false;
}