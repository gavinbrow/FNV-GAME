struct RegistryEntry;

extern RegistryEntry DAT_011b4df4;
extern RegistryEntry* DAT_011b4dfc;
extern RegistryEntry* DAT_01268790;

// @fnv 0x00fbeba0
void FUN_00fbeba0()
{
    DAT_011b4dfc = DAT_01268790;
    DAT_01268790 = &DAT_011b4df4;
}
