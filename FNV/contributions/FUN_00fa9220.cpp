struct GlobalTriple
{
    unsigned int value0;
    unsigned int value1;
    unsigned int value2;
};

struct GlobalMatrix3
{
    GlobalTriple row0;
    GlobalTriple row1;
    GlobalTriple row2;
};

extern GlobalMatrix3 DAT_011a9448;
extern GlobalMatrix3 DAT_011e09ec;

// @fnv 0x00fa9220
void FUN_00fa9220()
{
    DAT_011e09ec = DAT_011a9448;
}
