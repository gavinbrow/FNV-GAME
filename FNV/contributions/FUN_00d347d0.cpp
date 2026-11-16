extern float DAT_0104da48;
extern unsigned char DAT_010ce7fc;
extern "C" void __cdecl FUN_00d43960();

struct D347D0Query {
    const unsigned char* descriptor;
    float bound;
    unsigned int filter;
};

void __cdecl FUN_00d347d0(void* a, void* b, void* c, unsigned int filter)
{
    D347D0Query query = { &DAT_010ce7fc, DAT_0104da48, filter };
    typedef void (__cdecl *Dispatch)(void*, void*, void*, D347D0Query*);
    ((Dispatch)FUN_00d43960)(b, a, c, &query);
}
