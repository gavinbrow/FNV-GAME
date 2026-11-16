struct FUN_006299a0
{
    int value;

    FUN_006299a0();
    ~FUN_006299a0();
};

struct FUN_009b2cb0
{
    FUN_006299a0 unk00;
    int unk04;
    unsigned int unk08;
    int unk0c;

    FUN_009b2cb0(unsigned int a);
};

int __cdecl FUN_009b2e60(unsigned int a, unsigned int b);

FUN_006299a0::FUN_006299a0()
{
}

FUN_006299a0::~FUN_006299a0()
{
}

FUN_009b2cb0::FUN_009b2cb0(unsigned int a)
{
    unk00.value = FUN_009b2e60(a, 0);
    unk08 = a | 0x80000000u;
    unk0c = unk00.value;
}