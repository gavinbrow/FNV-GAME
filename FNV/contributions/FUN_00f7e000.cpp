struct GlobalObject_0040c150
{
    void* m_vtable;
    const char* m_name;
    const char* m_default;
    GlobalObject_0040c150(const char*, const char*);
};
extern "C" const char DAT_0101d92c;
extern "C" const char DAT_010640d0;
extern "C" const char DAT_010640c8;
extern "C" const char DAT_010640bc;
extern "C" const char DAT_0104843c;
extern "C" const char DAT_010640b0;
extern "C" const char DAT_010640a8;
extern "C" const char DAT_01064098;
extern "C" const char DAT_0101d924;
extern "C" const char DAT_0106408c;
extern "C" const char DAT_01064084;
extern "C" const char DAT_01064074;
extern "C" const char DAT_01048444;
extern "C" const char DAT_01064068;
extern "C" const char DAT_01064060;
extern "C" const char DAT_01064054;
extern "C" GlobalObject_0040c150* DAT_011d51b0;
extern "C" GlobalObject_0040c150* DAT_011d51b4;
extern "C" GlobalObject_0040c150* DAT_011d51b8;
extern "C" GlobalObject_0040c150* DAT_011d51bc;
extern "C" GlobalObject_0040c150* DAT_011d51c0;
extern "C" GlobalObject_0040c150* DAT_011d51c4;
extern "C" GlobalObject_0040c150* DAT_011d51c8;
extern "C" GlobalObject_0040c150* DAT_011d51cc;
// @fnv 0x00f7e000
void FUN_00f7e000()
{
    DAT_011d51b0 = new GlobalObject_0040c150(&DAT_010640d0, &DAT_0101d92c);
    DAT_011d51b4 = new GlobalObject_0040c150(&DAT_010640bc, &DAT_010640c8);
    DAT_011d51b8 = new GlobalObject_0040c150(&DAT_010640b0, &DAT_0104843c);
    DAT_011d51bc = new GlobalObject_0040c150(&DAT_01064098, &DAT_010640a8);
    DAT_011d51c0 = new GlobalObject_0040c150(&DAT_0106408c, &DAT_0101d924);
    DAT_011d51c4 = new GlobalObject_0040c150(&DAT_01064074, &DAT_01064084);
    DAT_011d51c8 = new GlobalObject_0040c150(&DAT_01064068, &DAT_01048444);
    DAT_011d51cc = new GlobalObject_0040c150(&DAT_01064054, &DAT_01064060);
}
