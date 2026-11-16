struct ThreeWords
{
    unsigned int a;
    unsigned int b;
    unsigned int c;
};

extern ThreeWords DAT_011f426c;
extern ThreeWords DAT_011deac0;

// @fnv 0x00fa32a0
void FUN_00fa32a0()
{
    DAT_011deac0.a = DAT_011f426c.a;
    DAT_011deac0.b = DAT_011f426c.b;
    DAT_011deac0.c = DAT_011f426c.c;
}
