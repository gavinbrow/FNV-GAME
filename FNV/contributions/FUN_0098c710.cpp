#include "h_74712c1d3c73.h"

struct DoorExtraFields {
    int formID;
    int refID;
    unsigned char unk08;
    unsigned char unk09;
    unsigned char unk0a;
};

struct CombatSearchMgr : FUN_0098c590_shell {
    void FUN_0098c710(int arg);
};

void CombatSearchMgr::FUN_0098c710(int arg)
{
    DoorExtraFields* door = (DoorExtraFields*)FUN_0098c590(arg);
    if (door != 0) {
        door->unk0a = 0;
        door->unk08++;
    }
}
