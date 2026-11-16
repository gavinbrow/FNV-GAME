struct ThreeWords
{
    unsigned int first;
    unsigned int second;
    unsigned int third;
};

extern ThreeWords DAT_011f426c;
extern ThreeWords DAT_011e0808;

// @fnv 0x00fa91f0
void FUN_00fa91f0()
{
    DAT_011e0808.first = DAT_011f426c.first;
    DAT_011e0808.second = DAT_011f426c.second;
    DAT_011e0808.third = DAT_011f426c.third;
}
