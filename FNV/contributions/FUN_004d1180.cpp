#include "h_08623abe54c0.h"
#include "h_0ff2f32892b1.h"

extern const double DAT_01020758;
extern char* DAT_011dea3c;
extern char DAT_01183128[];
extern char DAT_01183a34[];

bool __fastcall FUN_004d1360(char*);
float __cdecl FUN_0048ebc0(void*, bool);
void __cdecl FUN_005e58f0(int, char*, float*);
int __cdecl FUN_00ec43fb(void*, int, const char*, const char*, int);

struct ObjectForm {
    int FUN_00401170();
    float FUN_004be380(unsigned char);
};
struct InventoryEntry {
    void* pExtraObjectList;
    int iNumber;
    ObjectForm* pContainerObj;
    bool FUN_004bddd0(bool);
    unsigned char FUN_004bda70(int);
    int FUN_0044ddc0();
};
struct InventoryNode {
    InventoryEntry** FUN_006815c0();
    InventoryNode* FUN_00726070();
    bool FUN_008256d0();
};
struct ActorProcessView {
    BaseProcess* FUN_008d8520();
};
struct InventoryListView {
    InventoryNode* first;
    int FUN_004c8f30(int);
    float FUN_004d1180(ActorProcessView*);
};

float InventoryListView::FUN_004d1180(ActorProcessView* actor)
{
    float total = 0.0f;
    float weightModifier = 0.0f;
    InventoryNode* node = first;
    while (node && !node->FUN_008256d0() && *node->FUN_006815c0()) {
        InventoryEntry* item = *node->FUN_006815c0();
        ObjectForm* form = item->pContainerObj;
        if (item->FUN_004bddd0(false) && form->FUN_00401170() != 0x29) {
            if (form->FUN_00401170() == 0x28) {
                weightModifier = form->FUN_004be380(item->FUN_004bda70(4));
                if (weightModifier >= DAT_01020758) {
                    float factor = 1.0f;
                    FUN_005e58f0(0x49, DAT_011dea3c, &factor);
                    weightModifier *= factor;
                }
            } else {
                weightModifier = FUN_0048ebc0(form, FUN_004d1360(DAT_011dea3c));
            }
            int count = FUN_004c8f30(item->FUN_0044ddc0());
            if (form->FUN_00401170() == 0x18) {
                int evaluated = FUN_00ec43fb(form, 0, DAT_01183128, DAT_01183a34, 0);
            } else if (form->FUN_00401170() == 0x28) {
                BaseProcess* process = actor->FUN_008d8520();
                if (process) {
                    ItemChange* weapon = process->GetCurrentWeapon();
                    ItemChange* second = process->GetCurrentAmmo();
                    if (weapon && second &&
                        reinterpret_cast<InventoryEntry*>(weapon)->FUN_0044ddc0()
                        == reinterpret_cast<InventoryEntry*>(second)->FUN_0044ddc0()) {
                        count = 1;
                    }
                }
            }
            total += static_cast<float>(count) * weightModifier;
        }
        node = node->FUN_00726070();
    }
    return total;
}