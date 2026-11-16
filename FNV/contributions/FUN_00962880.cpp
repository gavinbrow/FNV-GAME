
struct EngineRoot; struct SceneManager; struct WorldData; struct ActionNode; struct ActionItem; struct InteractionHandler;
extern "C" EngineRoot* DAT_011dea3c;
struct EngineRoot { SceneManager* FUN_005d43c0(); };
struct SceneManager { WorldData* FUN_00422700(); };
struct WorldData { int flags; int status; int count; ActionNode* actions; };
struct ActionNode { ActionItem* item; ActionNode* next; ActionNode* ref_006815c0(); ActionNode* FUN_00726070(); };
struct ActionItem { InteractionHandler* FUN_008d8520(); };
struct InteractionHandler {
    virtual void slot0(); virtual void slot1(); virtual void slot2(); virtual void slot3();
    virtual void slot4(); virtual void slot5(); virtual void slot6(); virtual void slot7();
    virtual void slot8(); virtual void Process(ActionItem*,bool);
};
struct PlayerUIManager { void FUN_00962880(); };
void PlayerUIManager::FUN_00962880()
{
    WorldData* world = DAT_011dea3c->FUN_005d43c0()->FUN_00422700();
    if (world != 0 && world->actions != 0) {
        ActionNode* current = world->actions;
        while (current && current->ref_006815c0()->item != 0) {
            ActionNode* next = current->FUN_00726070();
            ActionItem* item = current->ref_006815c0()->item;
            if (item != 0 && item->FUN_008d8520() != 0) {
                item->FUN_008d8520()->Process(item, true);
                if (next != current->FUN_00726070())
                    current = world->actions;
                else
                    current = next;
            } else {
                current = next;
            }
        }
    }
}
