extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);
struct RefObject {
    virtual void UnknownVirtual();
    virtual void Destroy();
    volatile long referenceCount;
};
struct LODNode {
    unsigned int unknown00;
    unsigned int unknown04;
    unsigned int unknown08;
    unsigned int unknown0c;
    unsigned int unknown10;
    unsigned int unknown14;
    unsigned int unknown18;
    unsigned int unknown1c;
    unsigned int unknown20;
    unsigned int unknown24;
    unsigned int unknown28;
    unsigned int unknown2c;
    volatile unsigned int stateFlags;
    unsigned int unknown34;
    unsigned int unknown38;
    unsigned int unknown3c;
    unsigned int unknown40;
    unsigned int unknown44;
    unsigned int unknown48;
    unsigned int unknown4c;
    unsigned int unknown50;
    unsigned int unknown54;
    unsigned int unknown58;
    unsigned int unknown5c;
    unsigned int unknown60;
    unsigned int unknown64;
    unsigned int unknown68;
    unsigned int unknown6c;
    unsigned int unknown70;
    unsigned int unknown74;
    unsigned int unknown78;
    unsigned int unknown7c;
    unsigned int unknown80;
    unsigned int unknown84;
    unsigned int unknown88;
    unsigned int unknown8c;
    unsigned int unknown90;
    unsigned int unknown94;
    unsigned int unknown98;
    unsigned int unknown9c;
    unsigned int unknowna0;
    unsigned int unknowna4;
    unsigned int unknowna8;
    unsigned int unknownac;
    unsigned int unknownb0;
    unsigned int unknownb4;
    unsigned int unknownb8;
    RefObject* volatile activeReference;
};
struct NodeCollection {
    LODNode** elements;
    unsigned int capacity;
    unsigned int count;
};
struct LinkPair {
    LODNode* node;
    RefObject* reference;
};
struct PairCollection {
    LinkPair** elements;
    unsigned int capacity;
    unsigned int count;
};
struct LODManager : NiBoneLODController {
    void* unknown3c;
    NodeCollection** nodeGroups;
    unsigned short unknown44;
    unsigned short groupCount;
    void* unknown48;
    void* unknown4c;
    PairCollection** linkGroups;
    void* unknown54;
    void* unknown58;
    LODNode** defaultNodes;
    unsigned int unknown60;
    unsigned int defaultNodeCount;
    bool FUN_00a541f0(int desiredLOD);
};
bool LODManager::FUN_00a541f0(int desiredLOD)
{
    if (m_uiNumLODs > 0 && m_iLOD != desiredLOD &&
        (desiredLOD == -1 || (desiredLOD > -1 && (unsigned int)desiredLOD < m_uiNumLODs))) {

    bool enableFollowing = false;
    for (unsigned int groupIndex = 0; groupIndex < groupCount; ++groupIndex) {
        NodeCollection* group = nodeGroups[groupIndex];
        if (group) {
            if (groupIndex == (unsigned int)desiredLOD)
                enableFollowing = true;
            for (unsigned int i = 0; i < group->count; ++i) {
                LODNode* node = group->elements[i];
                if (enableFollowing)
                    node->stateFlags |= 2;
                else
                    node->stateFlags &= ~2u;
            }
        }
    }

    for (unsigned int i = 0; i < defaultNodeCount; ++i) {
        LODNode* node = defaultNodes[i];
        node->stateFlags = (node->stateFlags & ~2u) | 1u;
    }

    if (desiredLOD != -1) {
        PairCollection* group = linkGroups[desiredLOD];
        if (group) {
            for (unsigned int i = 0; i < group->count; ++i) {
                LODNode* node = group->elements[i]->node;
                node->stateFlags = (node->stateFlags & ~1u) | 2u;
                RefObject* newRef = group->elements[i]->reference;
                RefObject* oldRef = node->activeReference;
                if (oldRef != newRef) {
                    if (oldRef && InterlockedDecrement(&oldRef->referenceCount) == 0)
                        oldRef->Destroy();
                    node->activeReference = newRef;
                    if (newRef)
                        InterlockedIncrement(&newRef->referenceCount);
                }
            }
        }
    }

    m_iLOD = desiredLOD;
    return true;
    }
    return false;
}