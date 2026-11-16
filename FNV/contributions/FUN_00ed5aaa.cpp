// @fnv 0x00ed5aaa
int __cdecl FUN_00ed5aaa()
{
    short sw;
    __asm {
        fnstsw sw
        fnclex
    }
    return sw;
}
