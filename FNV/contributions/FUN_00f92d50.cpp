extern unsigned int PackRgba(unsigned int red, unsigned int green, unsigned int blue, unsigned int alpha);
extern unsigned int DAT_011dac50;
extern unsigned int DAT_011dac54;
extern unsigned int DAT_011dac58;
extern unsigned int DAT_011dac5c;

// @fnv 0x00f92d50
void FUN_00f92d50()
{
    DAT_011dac50 = PackRgba(0x1a, 0xff, 0x80, 0xff);
    DAT_011dac54 = PackRgba(0x2e, 0xcf, 0xff, 0xff);
    DAT_011dac58 = PackRgba(0xff, 0xb6, 0x42, 0xff);
    DAT_011dac5c = PackRgba(0xc5, 0xff, 0xff, 0xff);
}