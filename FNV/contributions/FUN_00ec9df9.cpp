extern "C" unsigned int __security_cookie;
extern unsigned int DAT_0126fda8;
// @fnv 0x00ec9df9
int FUN_00ec9df9()
{
    return DAT_0126fda8 == (__security_cookie | 1u);
}
