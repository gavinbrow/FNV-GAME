#include "h_3213349b7f9c.h"

void __cdecl FUN_004b6a00(NiCollisionObject*, CollisionObjectCountContext*);

struct FUN_004b6980_Context
{
    void* pCurrentObject;
    bool bRecurse;
    unsigned int uiTraversalFlags;
    void* pUserData;
    int iCount;
    void* pAuxiliaryData;
    unsigned int uiFilterFlags;
};

int __cdecl FUN_004b6980(NiAVObject* object, void* auxiliaryData, bool flag1, bool flag2, bool flag3)
{
    FUN_004b6980_Context context;

    context.uiTraversalFlags = 0x12;
    context.bRecurse = true;
    context.pUserData = 0;
    context.iCount = 0;
    context.pAuxiliaryData = auxiliaryData;
    context.uiFilterFlags = 0;

    if (flag1) {
        context.uiFilterFlags |= 1;
    }
    if (flag2) {
        context.uiFilterFlags |= 2;
    }
    if (flag3) {
        context.uiFilterFlags |= 4;
    }

    FUN_00c68900(object, reinterpret_cast<CollisionObjectCountContext*>(&context), FUN_004b6a00);

    return context.iCount;
}