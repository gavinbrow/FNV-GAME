class BGSSaveFormBuffer_Write : public BGSSaveFormBuffer {
public:
    void FUN_00865df0(TESObjectREFR* reference, unsigned int flag);
};
void __cdecl FUN_005aa930(BGSSaveFormBuffer* buffer)
{
    int count1;
    unsigned int offset1;
    BSSimpleList<TESObjectREFR*>* list1;
    {
    TESObjectREFR* item9;
    int count2;
    unsigned int offset6;
    BSSimpleList<TESObjectREFR*>* listVal;
    TESObjectREFR* aItem2;
    int count7;
    unsigned int offsetVal;
    BSSimpleList<TESObjectREFR*>* list9;
    TESObjectREFR* item8;
    int count9;
    {
    unsigned int offset4;
    BSSimpleList<TESObjectREFR*>* list4;
    TESObjectREFR* item6;

    DAT_011cacf8.FUN_004538a0(0);
    count1 = 0;
    offset1 = buffer->FUN_00865f20();
    list1 = &DAT_011caca8;
    while (list1 != 0) {
        item9 = (TESObjectREFR*)*FUN_006815c0(list1);
        if (item9 != 0) {
            ((BGSSaveFormBuffer_Write*)buffer)->FUN_00865df0(item9, 0);
            count1 = count1 + 1;
        }
        list1 = (BSSimpleList<TESObjectREFR*>*)FUN_00726070(list1);
    }
    buffer->FUN_00865ff0(count1, offset1);

    count2 = 0;
    offset6 = buffer->FUN_00865f20();
    listVal = &DAT_011cac98;
    while (listVal != 0) {
        aItem2 = (TESObjectREFR*)*FUN_006815c0(listVal);
        if (aItem2 != 0) {
            ((BGSSaveFormBuffer_Write*)buffer)->FUN_00865df0(aItem2, 0);
            count2 = count2 + 1;
        }
        listVal = (BSSimpleList<TESObjectREFR*>*)FUN_00726070(listVal);
    }
    buffer->FUN_00865ff0(count2, offset6);

    count7 = 0;
    offsetVal = buffer->FUN_00865f20();
    list9 = &DAT_011cacb8;
    while (list9 != 0) {
        item8 = (TESObjectREFR*)*FUN_006815c0(list9);
        if (item8 != 0) {
            ((BGSSaveFormBuffer_Write*)buffer)->FUN_00865df0(item8, 0);
            count7 = count7 + 1;
        }
        list9 = (BSSimpleList<TESObjectREFR*>*)FUN_00726070(list9);
    }
    buffer->FUN_00865ff0(count7, offsetVal);

    count9 = 0;
    offset4 = buffer->FUN_00865f20();
    list4 = &DAT_011cace8;
    while (list4 != 0) {
        item6 = (TESObjectREFR*)*FUN_006815c0(list4);
        if (item6 != 0) {
            ((BGSSaveFormBuffer_Write*)buffer)->FUN_00865df0(item6, 0);
            count9 = count9 + 1;
        }
        list4 = (BSSimpleList<TESObjectREFR*>*)FUN_00726070(list4);
    }
    buffer->FUN_00865ff0(count9, offset4);
    }
    }
    DAT_011cacf8.FUN_004538c0();}

