// @fnv 0x00fbf410
int PackBytesBigEndian(int first, int second, int third, int fourth);
extern "C" int DAT_01269018;

extern "C" void FUN_00fbf410()
{
    DAT_01269018 = PackBytesBigEndian(0x46, 200, 0x46, 0x8c);
}
