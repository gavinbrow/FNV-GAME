void __cdecl FUN_008324e0(bool enabled);
void __cdecl FUN_008331c0(bool enabled);
void __cdecl FUN_00836e20(int updateMode) {
    BSSimpleList<FalloutRadio::StationState*>* current = &DAT_011dd554;
    BSSimpleList<FalloutRadio::StationState*>* previous = 0;
    while (current != 0 && !current->IsEmpty()) {
        FalloutRadio::StationState* receiver = current->GetItem();
        bool remove = false;
        if (receiver != 0)
            reinterpret_cast<FUN_008366c0_shell*>(receiver)->FUN_008366c0(updateMode);
        else
            remove = true;
        if (remove) {
            if (previous != 0) {
                previous->Remove(current->GetItem());
                current = previous->GetNext();
            } else
                current->RemoveHead();
        } else {
            previous = current;
            current = current->GetNext();
        }
    }
    FUN_008324e0(DAT_011dd434);
    if (DAT_011dd42c != 0)
        FUN_008331c0(true);
}