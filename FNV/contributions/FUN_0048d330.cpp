class ActorPackage {
public:
    bool _ref_00440d80();
    unsigned int _ref_0084e3a0();
};
struct TESSpellListShell : TESSpellList {
    ListNode* _ref_00717e50();
    void FUN_0048d330();
};
void __cdecl FUN_00485910(unsigned int type, unsigned int formId);
void TESSpellListShell::FUN_0048d330()
{
    ListNode* currentLeveledSpell = _ref_00717e50();
    unsigned int currentSpell;
    ActorPackage* spell;
    while (currentLeveledSpell != 0 && (spell = currentLeveledSpell->_ref_006815c0()) != 0) {
        if (!spell->_ref_00440d80()) {
            currentSpell = spell->_ref_0084e3a0();
            FUN_00485910(0x4f4c5053, currentSpell);
        }
        currentLeveledSpell = currentLeveledSpell->_ref_00726070();
    }
    ListNode* leveledSpell = (ListNode*)FUN_0048d150();
    {
        ActorPackage* formId;
        while (leveledSpell != 0 && (formId = leveledSpell->_ref_006815c0()) != 0) {
            if (!formId->_ref_00440d80()) {
                unsigned int leveledFormId = formId->_ref_0084e3a0();
                FUN_00485910(0x4f4c5053, leveledFormId);
            }
            leveledSpell = leveledSpell->_ref_00726070();
        }
    }
}