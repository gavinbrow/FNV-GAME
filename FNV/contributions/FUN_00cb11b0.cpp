// unit_ff4bdaca3856.cpp

extern "C" {
    void* __cdecl FUN_00cb10d0(void* p);
    void* __cdecl FUN_00c85690(void* p, int n);
    void* __cdecl FUN_00cb10b0(void* p, void* q, int n);
}

void* __cdecl FUN_00cb11b0(void* p1, int n2, void* p3)
{
    int len = (int)FUN_00cb10d0(p1);
    if (len > n2)
        len = n2;

    void* buf = FUN_00c85690(p3, len + 1);
    FUN_00cb10b0(buf, p1, len);
    ((char*)buf)[len] = 0;
    return buf;
}
