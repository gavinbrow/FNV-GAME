struct GlobalObject {
    int unk00;
};
extern GlobalObject g_global;

GlobalObject* __cdecl FUN_00de8250()
{
    return &g_global;
}
