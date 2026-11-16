#include "h_ba4e959c9b7b.h"

struct GroupToHelpEntry {
    void* owner;
    CombatGroup* group;
};

bool HighProcess::FUN_008f5410(CombatGroup* group)
{
    bool found = false;
    BSSimpleList<TESTopicInfo*>* node = &GroupsToHelpList;
    while (node && node->GetItem() && !found)
    {
        TESTopicInfo* entry = node->GetItem();
        if (group == reinterpret_cast<GroupToHelpEntry*>(entry)->group)
            found = true;
        node = node->GetNext();
    }
    return found;
}