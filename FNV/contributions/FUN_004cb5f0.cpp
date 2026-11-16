extern float DAT_010162c0;
extern const char DAT_0101c178[];
extern const char DAT_01012058[];
extern const char DAT_0101dcc4[];
extern const char DAT_010207c0[];
extern const char DAT_010208e0[];

struct MoveActorExt : MoveOwner {
    bool FUN_008b8e90(MoveForm*);
};
const char* __cdecl FUN_0048e730(TESBoundObject*, MoveOwner*);
void __cdecl FUN_00406d00(char*, unsigned int, const char*, const char*, const char*);
struct InventoryMoveTarget : InventoryMove {
    void FUN_004cb5f0(MoveOwner*,MoveOwner*,MoveForm*);
};
void InventoryMoveTarget::FUN_004cb5f0(MoveOwner* source, MoveOwner* destination, MoveForm* onlyForm)
{
    MoveItem* item = 0;
    TESBoundObject* form = 0;
    MoveItemNode* itemNode = head;
    while (itemNode && !itemNode->FUN_008256d0()) {

        MoveItemNode* savedItemNext = itemNode->FUN_00726070();
        item = *itemNode->FUN_006815c0();
        bool restartItems = false;

        if (item && item->FUN_00726070() > 0 && !((MoveForm*)item->FUN_0044ddc0())->IsQuestItem()) {
            MoveExtraNode* pExtra = item->FUN_00559450();
            form = item->FUN_0044ddc0();
            MoveOwner* actor = 0;
            if (destination->IsActor())
                actor = destination;
            if (pExtra && *pExtra->FUN_006815c0()) {
                while (pExtra && *pExtra->FUN_006815c0() && !restartItems) {
                    MoveExtraNode* savedExtraNext2 = pExtra->FUN_00726070();
                    MoveExtra* extra = *pExtra->FUN_006815c0();
                    bool restartExtras = false;
                    MoveForm* original4 = (MoveForm*)extra->FUN_00418660();
                    MoveForm* baseExtraA = 0;
                    MoveForm* modExtra_2 = 0;
                    if (original4) {
                        if (original4->FUN_00401170() == 8)
                            modExtra_2 = original4;
                        else
                            baseExtraA = original4;
                    }

                    if (!onlyForm || onlyForm == (MoveForm*)extra->FUN_00418660()) {
                        if (actor && !onlyForm)
                            onlyForm = (MoveForm*)actor->FUN_007af430();
                        if (extra->FUN_00418660() &&
                            (MoveForm*)extra->FUN_00418660() != (MoveForm*)source &&
                            (!actor || actor->FUN_007af430() == baseExtraA ||
                             ((MoveActorExt*)actor)->FUN_008b8e90(modExtra_2))) {

                        if (item->FUN_00559450()->FUN_005ae380() <= 1)
                            restartItems = true;
                        else
                            restartExtras = true;

                        if (onlyForm) {
                            MoveString formattedItem;
                            int copies = extra->FUN_00418770();
                            if (copies > 1) {
                                FUN_00406f60(&formattedItem, DAT_0101c178, copies,
                                    FUN_00482720(form),
                                    moveVerb.FUN_00403df0(),
                                    movePlural.FUN_00403df0());
                            } else {
                                FUN_00406f60(&formattedItem, DAT_01012058,
                                    FUN_00482720(form),
                                    movePlural.FUN_00403df0());
                            }
                            char message4[260];
                            FUN_00406d00(message4, 260, DAT_0101dcc4, DAT_010207c0,
                                FUN_0048e730(form, inventoryPlayer));
                            FUN_007052f0(formattedItem.FUN_00559450(), 0, DAT_010208e0,
                                inventoryPlayer->FUN_008adcf0(form, false, false),
                                DAT_010162c0, 0);
                        }
                        FUN_004c37d0(source, form, false, extra->FUN_00418770(),
                                     extra, 0, destination, 0, 0, true, 0, 0);
                        itemNode = head;
                        }
                    }

                    if (restartItems) {
                        itemNode = head;
                        pExtra = 0;
                    } else if (restartExtras) {
                        pExtra = item->FUN_00559450();
                    } else {
                        if (savedExtraNext2 != pExtra->FUN_00726070())
                            pExtra = item->FUN_00559450();
                        else
                            pExtra = savedExtraNext2;
                        if (!pExtra) {
                            if (savedItemNext != itemNode->FUN_00726070())
                                itemNode = head;
                            else
                                itemNode = savedItemNext;
                        }
                    }
                }
            } else {
                if (savedItemNext != itemNode->FUN_00726070())
                    itemNode = head;
                else
                    itemNode = savedItemNext;
            }
        } else {
            if (savedItemNext != itemNode->FUN_00726070())
                itemNode = head;
            else
                itemNode = savedItemNext;
        }
    }
}
