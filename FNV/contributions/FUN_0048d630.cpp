// A nonvirtual stand-in for accessing spell-list methods whose names are unresolved.
struct SpellListAccess : TESSpellList {
    ListNode* FUN_00717e50();
    void FUN_0048d630(BaseFormComponent* source);
};

// Replace this object's two linked spell lists with the corresponding lists
// from another spell-list component, if the source is of the required type.
void SpellListAccess::FUN_0048d630(BaseFormComponent* source) {
    TESSpellList* a = dynamic_cast<TESSpellList*>(source); // source spell-list component
    if (a == 0) return;

    reinterpret_cast<FUN_0048d060*>(this)->ClearDataComponent();

    ListNode* f = reinterpret_cast<SpellListAccess*>(a)->FUN_00717e50(); // source spell nodes
    LH* b = reinterpret_cast<LH*>(FUN_00717e50()); // destination spell list
    SpellItem* d; // current spell
    while (f != 0) {
        d = reinterpret_cast<SpellItem*>(f->_ref_006815c0());
        if (d != 0) b->AddHead(d);
        f = f->_ref_00726070();
    }

    ListNode* e = reinterpret_cast<ListNode*>(a->FUN_0048d150()); // source leveled-spell nodes
    {
        LH* c = reinterpret_cast<LH*>(FUN_0048d150()); // destination leveled-spell list
        while (e != 0) {
            SpellItem* g = reinterpret_cast<SpellItem*>(e->_ref_006815c0()); // current entry
            if (g != 0) c->AddHead(g);
            e = e->_ref_00726070();
        }
    }
}