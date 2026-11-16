struct FUN_00ec78f1_t {
    int m0;
    int m4;
    void* __thiscall FUN_00ec78f1(int* out);
    
};
void __stdcall FUN_00ec7894(FUN_00ec78f1_t* info, const char* fmt);
void* __cdecl operator new(unsigned int);
extern int DAT_010176f8;
extern int DAT_01140ef8;

void* __cdecl FUN_00b23980(unsigned int n)
{
    int pad;
    if (!(n > 0))
        n = 0;
    else {
        if (-1u / n < 0x38) {
            FUN_00ec78f1_t o;
            {
                int zero = 0;
                o.FUN_00ec78f1(&zero);
            }
            o.m0 = (unsigned int)&DAT_010176f8;
            FUN_00ec7894(&o, (const char*)&DAT_01140ef8);
        }
    }
    return ::operator new(n * 0x38);
}