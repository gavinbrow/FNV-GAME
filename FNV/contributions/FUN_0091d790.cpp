struct InventoryItemLookup {
    void** FUN_006815c0();
};
struct InventoryLookup {
    InventoryItemLookup* FUN_00559450();
    void* FUN_0044ddc0(void* item, bool enabled);
};
struct ActorInventoryAccess {
    InventoryLookup* FUN_00891d30();
    void FUN_008c1de0(void* item);
};
struct FUN_0091d790_shell : MiddleHighProcess {
    bool FUN_0091d790(ActorInventoryAccess* actor);
};
bool FUN_0091d790_shell::FUN_0091d790(ActorInventoryAccess* actor) {
    InventoryLookup* inventory = 0;
    inventory = actor->FUN_00891d30();
    if (inventory != 0) {
        void* entry = 0;
        if (inventory->FUN_00559450() != 0) {
            entry = *inventory->FUN_00559450()->FUN_006815c0();
        }
        actor->FUN_008c1de0(inventory->FUN_0044ddc0(entry, true));
        AddToProcedureIndexRunning(reinterpret_cast<MobileObject*>(actor), 1);
    }
    return false;
}