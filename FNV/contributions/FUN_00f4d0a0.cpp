struct ThreeWords
{
    unsigned int a;
    unsigned int b;
    unsigned int c;
};

extern ThreeWords DAT_011f426c;
extern ThreeWords DAT_011ca7a8;

// @fnv 0x00f4d0a0
void FUN_00f4d0a0()
{
    DAT_011ca7a8.a = DAT_011f426c.a;
    DAT_011ca7a8.b = DAT_011f426c.b;
    DAT_011ca7a8.c = DAT_011f426c.c;
}
