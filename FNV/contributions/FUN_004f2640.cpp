struct NodeHeader { unsigned int unk00; };
struct NodeHolder : NodeHeader, RDLNode {};
struct QueryContext {
    void* unk00;
    void* unk04;
    unsigned int unk08;
    unsigned int unk0c;
};
struct RegionList {
    RDLNode* FUN_00413f40();
};
struct RegionContainer {
    RegionList* FUN_004f35b0();
};
struct RegionEntry {
    RegionContainer* FUN_009611e0(unsigned int);
};
struct InnerRegion {
    NodeHolder* FUN_00547110();
};
struct RegionSource {
    InnerRegion* FUN_00527900();
};
struct RegionPlayer {
    NodeHolder* FUN_004f2770();
    RegionSource* FUN_00575650(QueryContext*, bool);
};
extern TESObjectREFR* _g_thePlayer;

bool __cdecl FUN_004f2640(RDLItem* target)
{
    RDLNode* regionNode = reinterpret_cast<RegionPlayer*>(_g_thePlayer)->FUN_004f2770();
    RDLItem* listEntry;
    RegionList* childList;
    RegionList* listReference;
    RDLNode* entryNode;
    QueryContext queryBuffer;
    if (regionNode == 0 || *regionNode->FUN_006815c0() == 0)
    {
        regionNode = reinterpret_cast<RegionPlayer*>(_g_thePlayer)->FUN_00575650(&queryBuffer, true)
                   ->FUN_00527900()->FUN_00547110();
    }
    while (regionNode != 0 && *regionNode->FUN_006815c0() != 0)
    {
        listEntry = *regionNode->FUN_006815c0();
        if (listEntry != 0)
        {
            childList = reinterpret_cast<RegionEntry*>(listEntry)
                                   ->FUN_009611e0(8)->FUN_004f35b0();
            if (childList != 0)
            {
                listReference = childList;
                entryNode = listReference->FUN_00413f40();
                while (entryNode != 0)
                {
                    if (*entryNode->FUN_006815c0() != 0 &&
                        *entryNode->FUN_006815c0() == target)
                        return true;
                    entryNode = entryNode->FUN_00726070();
                }
            }
        }
        regionNode = regionNode->FUN_00726070();
    }
    return false;
}