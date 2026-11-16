void* __cdecl FUN_00aa1070(unsigned int a);
void* __cdecl memmove(void* d, const void* s, unsigned int n);
int __cdecl FUN_00aa0020(int a, int b, const char* c);

bool __stdcall FUN_00e98370(int a, int b, int* c, int* d, int* e, int* f, int g)
{
    *c = 0;
    *d = 0;
    *e = 0;
    *f = 0;
    if (a != 0 && b != 0)
    {
        void* r = FUN_00aa1070((unsigned int)b);
        *c = (int)r;
        memmove(r, (const void*)a, (unsigned int)b);
        *d = b;
        return true;
    }
    FUN_00aa0020(1, g, "Invalid shader buffer\n");
    return false;
}


