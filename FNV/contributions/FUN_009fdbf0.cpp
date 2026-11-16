void __stdcall FUN_009fdbf0(int a, int b, int c)
{
    void* p = *(void**)(a + 0x8c);
    typedef void (__thiscall *Method)(void*, int, int);
    Method m = (Method)(*(void***)p)[9];
    m(p, b, c);
}
