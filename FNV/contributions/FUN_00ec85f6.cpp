struct RegistryObject { unsigned int otherFields[3]; unsigned int value; };
extern "C" RegistryObject* __cdecl FUN_00ed1165();
extern "C" char DAT_011c18c4;
// @fnv 0x00ec85f6
extern "C" void* __cdecl FUN_00ec85f6()
{
    RegistryObject* current = FUN_00ed1165();
    if (!current) return &DAT_011c18c4;
    return &current->value;
}
