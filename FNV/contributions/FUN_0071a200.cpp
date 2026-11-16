
struct EntryProperty { int FUN_0044ddc0(); };
struct Entry { int id; EntryProperty* property; };
struct ListNode {
    Entry* item;
    ListNode* next;
    Entry** FUN_006815c0();
    ListNode* FUN_00726070();
};
struct TemporaryList : ListNode {
    TemporaryList();
    ~TemporaryList();
    void FUN_005ae3d0(Entry** item);
    void FUN_00470470();
};
struct FunctionOwner {
    int unk00;
    ListNode entries;
    void FUN_0071a5c0(int id);
    void FUN_0071a200(int entryType);
};
void FunctionOwner::FUN_0071a200(int entryType)
{
    TemporaryList selected;
    {
        ListNode* matched;
        ListNode* current;
        current = this ? &entries : 0;
        for (; current && *current->FUN_006815c0(); current = current->FUN_00726070()) {
            if ((*current->FUN_006815c0())->property) {
                if ((*current->FUN_006815c0())->property->FUN_0044ddc0() == entryType) {
                    selected.FUN_005ae3d0(current->FUN_006815c0());
                }
            }
        }
        matched = &selected;
        for (; matched && *matched->FUN_006815c0(); matched = matched->FUN_00726070()) {
            FUN_0071a5c0((*matched->FUN_006815c0())->id);
        }
    }
    selected.FUN_00470470();
}
