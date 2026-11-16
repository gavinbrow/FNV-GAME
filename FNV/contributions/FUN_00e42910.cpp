struct FUN_00e37940_Item {
    void FUN_00e37940();
};
struct FUN_00e42910_List {
    unsigned int unk00;
    unsigned int unk04;
    FUN_00e37940_Item** items;
    int count;
    void FUN_00e42910();
};
void FUN_00e42910_List::FUN_00e42910()
{
    int countSnapshot = count;
    for (int index=0;index<countSnapshot;++index)
        items[index]->FUN_00e37940();
}