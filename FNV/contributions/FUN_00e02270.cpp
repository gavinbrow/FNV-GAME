struct GlobalObject {
    int unk00;
};
extern GlobalObject g_global;

GlobalObject* __cdecl FUN_00e02270()
{
    return &g_global;
}
