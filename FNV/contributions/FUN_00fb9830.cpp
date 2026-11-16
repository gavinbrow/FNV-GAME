struct InitializerPair
{
    unsigned int first;
    unsigned int second;
};

extern InitializerPair DAT_011f4980;
extern InitializerPair DAT_011f9634;

// @fnv 0x00fb9830
void FUN_00fb9830()
{
    DAT_011f9634.first = DAT_011f4980.first;
    DAT_011f9634.second = DAT_011f4980.second;
}
