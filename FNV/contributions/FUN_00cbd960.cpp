// FUN_00cbd960 registers the 0x00cbd7a0 comparison helper in the global
// callback slot at 0x01268430, which is later called indirectly with two
// arguments (see the indirect call through 0x01268430).
extern void (__cdecl *DAT_01268430)(void*, void*);

void __cdecl FUN_00cbd7a0(void* pList, void* pContext);

void __cdecl FUN_00cbd960(void)
{
    DAT_01268430 = &FUN_00cbd7a0;
}
