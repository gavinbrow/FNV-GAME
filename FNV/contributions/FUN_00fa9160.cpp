struct ThreeWords
{
    unsigned int first;
    unsigned int second;
    unsigned int third;
};

extern ThreeWords DAT_011f426c;
extern ThreeWords DAT_011e0b58;

// @fnv 0x00fa9160
void FUN_00fa9160()
{
    DAT_011e0b58.first = DAT_011f426c.first;
    DAT_011e0b58.second = DAT_011f426c.second;
    DAT_011e0b58.third = DAT_011f426c.third;
}
