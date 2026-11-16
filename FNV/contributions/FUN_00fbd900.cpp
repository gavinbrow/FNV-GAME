struct UnrecoveredRegistryEntry;

extern UnrecoveredRegistryEntry DAT_011b0f00;
extern UnrecoveredRegistryEntry* DAT_011b0f08;
extern UnrecoveredRegistryEntry* DAT_01268790;

// @fnv 0x00fbd900
void FUN_00fbd900()
{
    DAT_011b0f08 = DAT_01268790;
    DAT_01268790 = &DAT_011b0f00;
}
