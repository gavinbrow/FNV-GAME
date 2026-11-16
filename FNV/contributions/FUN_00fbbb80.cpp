struct InitializerTriple
{
    unsigned int first;
    unsigned int second;
    unsigned int third;
};

extern InitializerTriple DAT_011f426c;
extern InitializerTriple DAT_01202e68;

// @fnv 0x00fbbb80
void FUN_00fbbb80()
{
    DAT_01202e68.first = DAT_011f426c.first;
    DAT_01202e68.second = DAT_011f426c.second;
    DAT_01202e68.third = DAT_011f426c.third;
}
