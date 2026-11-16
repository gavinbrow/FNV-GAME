struct UnrecoveredRegistryEntry;

extern UnrecoveredRegistryEntry DAT_011b8330;
extern UnrecoveredRegistryEntry* DAT_011b8338;
extern UnrecoveredRegistryEntry* DAT_01268790;

// @fnv 0x00fc0160
void FUN_00fc0160()
{
    DAT_011b8338 = DAT_01268790;
    DAT_01268790 = &DAT_011b8330;
}
