struct ChangeItem { void* FUN_0044ddc0(); ~ChangeItem(); };
struct InventoryIterator { ~InventoryIterator(); };
struct MatchedChanges { void FUN_005ae3d0(ChangeItem** item); };
bool __cdecl FUN_0047bb50(void* itemForm, void* requestedForm);
struct InventoryChangeFilterHost {
  InventoryIterator* FUN_004ca200();
  ChangeItem* FUN_004ca330(InventoryIterator* iterator);
  void FUN_004d4bd0(void* requestedForm, MatchedChanges* matchedChanges);
};
void InventoryChangeFilterHost::FUN_004d4bd0(void* requestedForm, MatchedChanges* matchedChanges) {
    if (!requestedForm || !matchedChanges) return;

    InventoryIterator* iterator = FUN_004ca200();
    ChangeItem* itemChange = 0;
    do {
       itemChange = FUN_004ca330(iterator);
       if (itemChange) {
          if (FUN_0047bb50(itemChange->FUN_0044ddc0(), requestedForm))
             matchedChanges->FUN_005ae3d0(&itemChange);
          else
             delete itemChange;
       }
    } while (itemChange);
    delete iterator;
}