struct FUN_00481d10_shell : TESContainer { bool FUN_00481d10(BaseFormComponent* other); };
void* __fastcall _ref_00717e50(void*);
int __fastcall _ref_005ae380(void*);
bool FUN_00481d10_shell::FUN_00481d10(BaseFormComponent* other) {
    TESContainer* otherContainer = dynamic_cast<TESContainer*>(other);
    if (otherContainer == 0) return true;
    int matchCount = 0;
    void* current = _ref_00717e50(this);
    void* otherCurrent = 0;
    ContainerObject* itemBeingChecked;
    while (current != 0) {
        itemBeingChecked = *_ref_006815c0(current);
        if (itemBeingChecked != 0) {
            otherCurrent = _ref_00717e50(otherContainer);
            bool differenceFound = false;
            while (otherCurrent != 0) {
                ContainerObject* compareItem = *_ref_006815c0(otherCurrent);
                if (compareItem != 0) {
                    if (!reinterpret_cast<FUN_00481470_shell*>(compareItem)->FUN_00481470(itemBeingChecked)) {
                        differenceFound = true;
                        break;
                    }
                }
                otherCurrent = _ref_00726070(otherCurrent);
            }
            if (!differenceFound) return true;
            ++matchCount;
        }
        current = _ref_00726070(current);
    }
    if (_ref_005ae380(_ref_00717e50(otherContainer)) != matchCount) return true;
    return false;
}