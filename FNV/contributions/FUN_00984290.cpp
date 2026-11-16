struct FUN_00984290
{
    BSSimpleList<void*> first;
    BSSimpleList<void*> second;

    virtual ~FUN_00984290();
};

FUN_00984290::~FUN_00984290()
{
    BSSimpleList<void*>* list3;
    void* firstCurrent;
    void* firstItem4;
    void* secondCurrent;
    void* secondItem;

    list3 = &first;
    while (list3 != 0 && list3->GetItem() != 0)
    {
        firstCurrent = list3->GetItem();
        firstItem4 = firstCurrent;
        ::operator delete(firstItem4);
        list3->RemoveHead();
    }

    list3 = &second;
    while (list3 != 0 && list3->GetItem() != 0)
    {
        secondCurrent = list3->GetItem();
        secondItem = secondCurrent;
        ::operator delete(secondItem);
        list3->RemoveHead();
    }
}
