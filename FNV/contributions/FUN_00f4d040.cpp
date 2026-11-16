struct ThreeWords
{
    unsigned int first;
    unsigned int second;
    unsigned int third;
};

extern ThreeWords DAT_011f426c;
extern ThreeWords DAT_011ca77c;

// @fnv 0x00f4d040
void FUN_00f4d040()
{
    DAT_011ca77c.first = DAT_011f426c.first;
    DAT_011ca77c.second = DAT_011f426c.second;
    DAT_011ca77c.third = DAT_011f426c.third;
}
