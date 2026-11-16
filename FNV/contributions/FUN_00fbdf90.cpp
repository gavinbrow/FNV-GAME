struct GlobalLink;

extern GlobalLink DAT_011b2024;
extern GlobalLink* DAT_011b202c;
extern GlobalLink* DAT_01268790;

// @fnv 0x00fbdf90
void FUN_00fbdf90()
{
    DAT_011b202c = DAT_01268790;
    DAT_01268790 = &DAT_011b2024;
}
