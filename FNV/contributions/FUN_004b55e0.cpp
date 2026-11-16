struct FNVForm {
    int __thiscall FUN_00441110();
};

extern void* __cdecl FUN_00438220();

struct FNVNode {
    virtual void R00();
    virtual void R04();
    virtual void R08();
    virtual int IsBranch();
    virtual void R10();
    virtual void R14();
    virtual int IsLeaf();

    unsigned int __thiscall FUN_0043b480();
    FNVNode* __thiscall FUN_0043b4a0(unsigned int index);
    FNVForm* __thiscall FUN_00a59d30(void* context);
};

unsigned int __cdecl FUN_004b55e0(FNVNode* root)
{
    unsigned int found = 0;
    if (root->FUN_0043b480() == 0)
        return 0;

    unsigned int count = root->FUN_0043b480();
    for (unsigned int index = 0; index < count; ++index) {
        if (found != 0)
            return found;

        FNVNode* node = root->FUN_0043b4a0(index);
        if (node == 0)
            continue;

        if (node->IsBranch()) {
            FNVNode* branch = node;
            found = FUN_004b55e0(branch);
        } else if (node->IsLeaf()) {
            FNVNode* leaf = node;
            FNVForm* form = leaf->FUN_00a59d30(FUN_00438220());
            if (form != 0) {
                unsigned int accepted = (unsigned int)form &
                    ((form == 0 ? 0
                        : (form->FUN_00441110() >= 8 &&
                           form->FUN_00441110() <= 12)) ? ~0u : 0u);
                if (accepted)
                    return accepted;
            }
        }
    }

    return found;
}
