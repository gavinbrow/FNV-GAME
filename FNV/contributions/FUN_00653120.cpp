struct NiNode;
struct NiAVObjectLike { void** vtable; };
extern "C" NiAVObjectLike* __cdecl FUN_00607310(void*);
extern "C" NiNode* __cdecl FUN_00653180(void*);
typedef NiAVObjectLike* (__thiscall *FUN_00653120_vfunc_type)(NiAVObjectLike*);
typedef NiNode* (__thiscall *FUN_00653180_type)(void*);
NiNode* __cdecl FUN_00653120(void* apGeom)
{
    NiAVObjectLike* pNode = FUN_00607310(apGeom);
    NiNode* pObject;
    if (pNode != 0 && ((FUN_00653120_vfunc_type)pNode->vtable[0x94 / 4])(pNode) != 0)
    {
        pObject = ((FUN_00653180_type)FUN_00653180)(((FUN_00653120_vfunc_type)pNode->vtable[0x94 / 4])(pNode));
    }
    else
    {
        pObject = 0;
    }
    return pObject;
}