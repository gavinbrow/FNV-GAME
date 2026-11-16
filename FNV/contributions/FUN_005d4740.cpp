extern "C" unsigned char __cdecl FUN_005accb0(unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, unsigned int, float*);
extern const double DAT_01012060;
unsigned char __cdecl FUN_005d4740(unsigned int first, unsigned int second, unsigned int third, unsigned int fourth, unsigned int fifth, unsigned int sixth, unsigned int seventh, unsigned int eighth)
{
    float position = 0.0f;
    if (!FUN_005accb0(first, second, eighth, third, fourth, fifth, sixth, &position))
        return false;
    unsigned int initialScale = 0x100000;
    if (position > DAT_01012060) {
        unsigned int computedScale = (unsigned int)position << 20;
    }
    return true;
}