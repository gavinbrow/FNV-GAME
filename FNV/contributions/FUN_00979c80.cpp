void __cdecl Deallocate(void*);

struct ItemNode {
    void* value;
    ItemNode* next;
};

struct ItemList {
    ItemNode* first;
    ItemNode* last;

    ItemNode* __thiscall ref_006815c0();
    void __thiscall FUN_0063f7b0();
    void __thiscall FUN_007b9000();
    ~ItemList() { FUN_007b9000(); }
};

struct FUN_00979c80 {
    virtual ~FUN_00979c80();

    ItemList actions;
    ItemList states;
    ItemList targets;
    ItemList effects;
};

FUN_00979c80::~FUN_00979c80()
{
    ItemList* list = &targets;

    // Keep the retrieved values and the pointers being released in separate scopes.
    {
        void *current1, *current2, *current3, *current4;
        {
            void *owned1, *owned2, *owned3, *owned4;

            while (list != 0 && list->ref_006815c0()->value != 0) {
                current4 = list->ref_006815c0()->value;
                owned3 = current4;
                Deallocate(owned3);
                list->FUN_0063f7b0();
            }

            list = &actions;

            while (list != 0 && list->ref_006815c0()->value != 0) {
                current1 = list->ref_006815c0()->value;
                owned1 = current1;
                Deallocate(owned1);
                list->FUN_0063f7b0();
            }

            list = &states;

            while (list != 0 && list->ref_006815c0()->value != 0) {
                current2 = list->ref_006815c0()->value;
                owned4 = current2;
                Deallocate(owned4);
                list->FUN_0063f7b0();
            }

            list = &effects;

            while (list != 0 && list->ref_006815c0()->value != 0) {
                current3 = list->ref_006815c0()->value;
                owned2 = current3;
                Deallocate(owned2);
                list->FUN_0063f7b0();
            }
        }
    }
}