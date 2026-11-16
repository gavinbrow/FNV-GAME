#include "h_488030e7e838.h"

extern "C" int DAT_011dea3c;
extern "C" int DAT_011da348;
extern "C" int DAT_011da344;
extern "C" float DAT_0101e704;
extern "C" float DAT_01023cd8;

extern "C" void __cdecl FUN_004ff1a0(int, void*, int);
extern unsigned int __cdecl FUN_0079c070();
extern BSSimpleList<unsigned int>* __cdecl FUN_0079c080();
extern bool FUN_0079be30(RefH*);
extern int __cdecl FUN_0079bd70(FUN_0079bd70_data*, FUN_0079bd70_data*);

struct RadioEntry {
    unsigned int FUN_0055d520();
};
struct RadioTile : Tile {
    void FUN_00707e10(unsigned int);
};
struct UIRecord : BSStringT<char> {
    bool FUN_005f65d0(unsigned int*);
    void FUN_00470470();
};
struct RadioList {
    void** vtable;
    void* FUN_007a3820(RadioEntry*, unsigned int, int, int);
    void FUN_007a3d20(bool (*)(RefH*));
};
typedef void (__thiscall* RadioMethod)(RadioList*);
typedef void (__thiscall* RadioCallback)(RadioList*, void*);
struct FUN_0079bea0_Shell : MapMenu {
    void FUN_0079bea0();
};
void FUN_0079bea0_Shell::FUN_0079bea0() {
    UIRecord record;
    FUN_004ff1a0(DAT_011dea3c, &record, 0);
    ((RadioMethod)((RadioList*)&lbRadioStationsList)->vtable[7])((RadioList*)&lbRadioStationsList);
    for (BSSimpleList<unsigned int>* node = FUN_0079c080(); node && node->GetItem(); node = node->GetNext()) {
        RadioTile* tile = (RadioTile*)((RadioList*)&lbRadioStationsList)->FUN_007a3820(
            (RadioEntry*)node->GetItem(), ((RadioEntry*)node->GetItem())->FUN_0055d520(), 0, 0);
        tile->Set(0xfaa, 0x19);
        tile->FUN_00707e10(((RadioEntry*)node->GetItem())->FUN_0055d520());
        tile->Set(DAT_011da348, FUN_0079c070() &&
            node->GetItem() == *(unsigned int*)FUN_0079c070());
        tile->Set(DAT_011da344, record.FUN_005f65d0(&node->GetItem()) ? DAT_01023cd8 : DAT_0101e704, true);
    }
    ((RadioList*)&lbRadioStationsList)->FUN_007a3d20(&FUN_0079be30);
    ((RadioCallback)((RadioList*)&lbRadioStationsList)->vtable[8])((RadioList*)&lbRadioStationsList, (void*)&FUN_0079bd70);
    record.FUN_00470470();
}