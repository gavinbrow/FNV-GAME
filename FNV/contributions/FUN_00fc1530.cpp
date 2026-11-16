extern volatile unsigned int DAT_011b9e78;
extern volatile unsigned int DAT_011b9e7c;
extern volatile unsigned int DAT_011b9f78;
extern volatile unsigned int DAT_011b9f90;
extern volatile unsigned int DAT_011b9fa8;
extern volatile unsigned int DAT_011b9fc0;

// @fnv 0x00fc1530
void __cdecl FUN_00fc1530()
{
    unsigned int value = DAT_011b9e78;
    DAT_011b9f78 = value;
    value = DAT_011b9e7c;
    DAT_011b9f90 = value;
    DAT_011b9fa8 = value;
    DAT_011b9fc0 = value;
}
