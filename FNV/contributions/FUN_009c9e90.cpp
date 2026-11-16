extern TESObjectREFR* DAT_011f21cc;

struct FUN_009c9e90_shell : public VATS {
    void FUN_009c9e90(TESObjectREFR* target);
};

void FUN_009c9e90_shell::FUN_009c9e90(TESObjectREFR* target) {
    if (target == DAT_011f21cc)
        DAT_011f21cc = 0;

    BSSimpleList<VATS_COMMAND*>* current = &commandList;
    BSSimpleList<VATS_COMMAND*>* previous = 0;
    while (current != 0 && !current->IsEmpty()) {
        VATS_COMMAND* command = current->GetItem();
        if (command->pTarget == target) {
            VATS_COMMAND* temporary = command;
            VATS_COMMAND* deleting = temporary;
            deleting ? reinterpret_cast<StandIn*>(deleting)->FUN_009c8870(1) : 0;

            if (previous) {
                previous->Remove(command);
                current = previous->GetNext();
            } else {
                current->RemoveHead();
            }
        } else {
            previous = current;
            current = current->GetNext();
        }
    }
}