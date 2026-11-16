struct GlobalObject { int unk00; };
extern GlobalObject g_global;

GlobalObject* __cdecl FUN_00c8a790()
{
    return &g_global;
}
