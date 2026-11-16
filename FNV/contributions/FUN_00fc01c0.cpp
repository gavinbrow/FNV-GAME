struct GlobalLink;

extern GlobalLink DAT_011b8660;
extern GlobalLink* DAT_011b8668;
extern GlobalLink* DAT_01268790;

// @fnv 0x00fc01c0
void FUN_00fc01c0()
{
    DAT_011b8668 = DAT_01268790;
    DAT_01268790 = &DAT_011b8660;
}
