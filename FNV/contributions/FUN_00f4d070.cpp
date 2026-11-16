struct ThreeWords
{
    unsigned int a;
    unsigned int b;
    unsigned int c;
};

extern ThreeWords DAT_011f426c;
extern ThreeWords DAT_011ca75c;

// @fnv 0x00f4d070
void FUN_00f4d070()
{
    DAT_011ca75c.a = DAT_011f426c.a;
    DAT_011ca75c.b = DAT_011f426c.b;
    DAT_011ca75c.c = DAT_011f426c.c;
}
