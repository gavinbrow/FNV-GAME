void* __fastcall _ref_00717e50(void* pList);
void __fastcall _ref_0063f7b0(void* pList);
unsigned int __cdecl _ref_004839c0(unsigned int aFormID);

struct FUN_0048c930_shell {
    void FUN_0048c930(unsigned int flags, unsigned int unused);
};

void FUN_0048c930_shell::FUN_0048c930(unsigned int flags, unsigned int unused) {
    if (flags & 4) {
        void* iter = _ref_00717e50(this);
        int count = 0;
        while (iter != 0) {
            GROUP_REACTION_dummy* entry = *_ref_006815c0(iter);
            if (entry != 0) {
                unsigned int formID = (unsigned int)entry->pForm;
                entry->pForm = (TESForm*)_ref_004839c0(formID);
                if (entry->pForm == 0) {
                    _ref_0063f7b0(iter);
                    GROUP_REACTION_dummy* dead = entry;
                    operator delete(dead);
                } else {
                    iter = _ref_00726070(iter);
                }
            } else {
                iter = _ref_00726070(iter);
            }
        }
    }
}