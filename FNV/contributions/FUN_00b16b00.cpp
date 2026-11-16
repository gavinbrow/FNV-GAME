extern "C" char DAT_010176f8[];
extern "C" char DAT_01140ef8[];
extern "C" void __stdcall FUN_00ec7894(void* err2, const char* msg);

struct FUN_00b108e0_err {
    void* m_vptr;
    unsigned int unk04;
    unsigned int unk08;
    void FUN_00ec78f1(unsigned int* out);
};

int* FUN_00b16b00(unsigned int count, int zero)
{
    if (count <= 0)
        count = 0;
    else if (0xffffffffu / count < 4) {
        FUN_00b108e0_err val;
        unsigned int err = 0;
        val.FUN_00ec78f1(&err);
        val.m_vptr = DAT_010176f8;
        FUN_00ec7894(&val, DAT_01140ef8);
    }
    return (int*)operator new(count << 2);
}
