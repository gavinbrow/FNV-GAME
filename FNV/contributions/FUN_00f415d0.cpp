struct GlobalTriple
{
    unsigned int value0;
    unsigned int value1;
    unsigned int value2;
};

extern GlobalTriple DAT_011f4998;
extern GlobalTriple DAT_011c74b8;

// @fnv 0x00f415d0
void FUN_00f415d0()
{
    DAT_011c74b8 = DAT_011f4998;
}
