struct GlobalTriple
{
    unsigned int value0;
    unsigned int value1;
    unsigned int value2;
};

extern GlobalTriple DAT_011f426c;
extern GlobalTriple DAT_011e08f4;

// @fnv 0x00fa9190
void FUN_00fa9190()
{
    DAT_011e08f4 = DAT_011f426c;
}
