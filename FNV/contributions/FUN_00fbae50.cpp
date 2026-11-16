struct InitializerPair
{
    unsigned int first;
    unsigned int second;
};

extern InitializerPair DAT_011f4980;
extern InitializerPair DAT_012023f4;

// @fnv 0x00fbae50
void FUN_00fbae50()
{
    DAT_012023f4.first = DAT_011f4980.first;
    DAT_012023f4.second = DAT_011f4980.second;
}
