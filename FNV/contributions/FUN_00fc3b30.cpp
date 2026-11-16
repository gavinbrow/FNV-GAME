// @fnv 0x00fc3b30
extern "C" int DAT_011bc1f8;
extern "C" int DAT_011bc270;
extern "C" int DAT_011bc288;
extern "C" int DAT_011bc1fc;
extern "C" int DAT_011bc2b8;

extern "C" void FUN_00fc3b30()
{
    int value = DAT_011bc1f8;
    DAT_011bc270 = value;
    DAT_011bc288 = value;
    DAT_011bc2b8 = DAT_011bc1fc;
}