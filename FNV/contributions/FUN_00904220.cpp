// FNV decomp candidate: FUN_00904220 (web_clm_0c8c8f2d0c904a6d961a)
// __thiscall(this, int) ret 4: walks list at this+0x44c; on item->f30 == param,
// removes via node->_ref_00905330(&item) and frees via _Deallocate.

struct Item { char _pad[0x30]; int f30; };

void _Deallocate(void*);
void** __fastcall FUN_006815c0(void*);
void* __fastcall FUN_00726070(void*);

struct FUN_00904220_class {
    char _pad[0x44c];
    List_008d8ba0* f44c;
    void FUN_00904220(int aiID);
};

void FUN_00904220_class::FUN_00904220(int aiID) {
    void* node = this->f44c;
    bool found = false;
    while (node != 0 && *FUN_006815c0(node) != 0) {
        void* item = *FUN_006815c0(node);
        if (((Item*)item)->f30 == aiID) {
            this->f44c->_ref_00905330(item);
            void* tmp = item;
            _Deallocate(tmp);
            return;
        } else {
            node = FUN_00726070(node);
        }
    }
}
