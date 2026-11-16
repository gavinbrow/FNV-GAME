extern unsigned int DAT_011ffa6c;
void __cdecl FUN_00b97ed0(unsigned char param_1, int param_2)
{
    unsigned int index = DAT_011ffa6c;
    if (DAT_011ff9d8[index] == 0) {
        GetDispatcher(DAT_011f9508)->Notify(0xf, param_1, 0, 0);
    }
    DAT_011ff9d8[index] += param_2;
}
