

extern const char g_inventoryChangesSourceFilename[];

struct BoundShell : TESBoundObject {

    int FUN_00401170();

    bool FUN_004c0bf0();

    int FUN_00482a90();

};

struct ExtraShell : ExtraDataList {

    ExtraShell();

    bool FUN_00418750();

    short FUN_00418770();

    bool FUN_004127e0(ExtraShell*);

    void FUN_00419ad0(int);

    void FUN_00411ec0(ExtraShell*);

    signed char FUN_0042de90();

    void FUN_0042dec0();

};

struct ExtraNodeShell : BSSimpleList<ExtraDataList*> {

    ExtraNodeShell();

    ExtraShell** _ref_006815c0();

    ExtraNodeShell* _ref_00726070();

    bool FUN_005f65d0(ExtraShell**);

    void FUN_005ae3d0(ExtraShell**);

};

struct ItemShell : ItemChange {

    ItemShell(BoundShell*,int);

    int FUN_004bc8f0(bool);

    int FUN_004bc980();

    bool FUN_004bddd0(bool);

};

struct ItemListShell : BSSimpleList<ItemChange*> {

    void _ref_00905820(ItemChange**);

};

struct RefShell : TESObjectREFR {

    void Invalidate(unsigned mask) {

        typedef void (__thiscall *Callback)(TESObjectREFR*, unsigned);

        ((Callback)(*(void***)this)[18])(this,mask);

    }

};

struct ChangesShell : InventoryChanges {

    ItemShell* FUN_004bfba0(BoundShell*,int,int);

    BoundShell* FUN_004bffb0(BoundShell*);

    void FUN_004c1520(BoundShell*,int,int,ExtraShell*,ExtraNodeShell**);

};

void ChangesShell::FUN_004c1520(BoundShell* item, int number, int unknown, ExtraShell* selection, ExtraNodeShell** result)

{

    AutoMemContext contextGuard((MEM_CONTEXT)0x36, true, g_inventoryChangesSourceFilename, 0xb83);

    if (pRef) pRef->MarkAsModified(0x20);

    ItemShell* itemCount = FUN_004bfba0(item, 1, 0);

    int wornCount = FUN_004bffb0(item)->FUN_00482a90();

    int itemChange = wornCount;

    if (itemCount)

        itemChange += itemCount->iNumber;

    int oldCount = 0;

    if (itemCount && itemCount->pExtraObjectList) {

        oldCount = itemCount->FUN_004bc8f0(false) + itemCount->FUN_004bc980();

    }

    int needExtra = itemChange - oldCount;

    if (itemCount && itemCount->pExtraObjectList) {

        if (*((ExtraNodeShell*)itemCount->pExtraObjectList)->_ref_006815c0() &&

            (*((ExtraNodeShell*)itemCount->pExtraObjectList)->_ref_006815c0())->FUN_00418750())

            needExtra = wornCount - oldCount;

        bool found = false;

        if (selection && !((ExtraNodeShell*)itemCount->pExtraObjectList)->FUN_005f65d0(&selection)) {

            ExtraNodeShell* cursor = (ExtraNodeShell*)itemCount->pExtraObjectList;

            while (cursor && *cursor->_ref_006815c0()) {

                ExtraShell* possible = *cursor->_ref_006815c0();

                if (possible && !possible->FUN_004127e0(selection)) {
                    selection=possible;
                    found=true;
                    break;
                } else {
                    cursor = cursor->_ref_00726070();
                }

            }

            if (!found) selection = 0;

        }

    }

    bool remaining = true;

    ExtraShell* chosen = 0;

    if ((!selection && needExtra > 0) || !itemCount) {

        if (!itemCount) {

            itemCount = new ItemShell(item, 0);

            remaining = true;

            ((ItemListShell*)pListofChanges)->_ref_00905820((ItemChange**)&itemCount);

            selection = 0;

        }

    } else {

        if (itemCount->FUN_004bddd0(false))

            return;

        ExtraNodeShell* cursor = (ExtraNodeShell*)itemCount->pExtraObjectList;

        while (cursor && remaining) {

            chosen = *cursor->_ref_006815c0();

            if (selection && selection == chosen) {

                bool isWeapon = item->FUN_00401170() == 0x28 && item->FUN_004c0bf0();

                if (chosen->FUN_00418770() > 1 && item->FUN_00401170() != 0x29 && !isWeapon) {

                    selection = new ExtraShell();

                    selection->FUN_00411ec0(chosen);

                    selection->FUN_00419ad0(1);

                    chosen->FUN_00419ad0(chosen->FUN_00418770() - 1);

                    if (chosen->FUN_0042de90() >= 0)

                        chosen->FUN_0042dec0();

                } else {

                    chosen->FUN_00419ad0((int)((ExtraNodeShell*)itemCount)->_ref_00726070());

                }

                remaining = false;

            } else if (chosen && !selection) {

                if (chosen->FUN_00418770() == 1) {

                    selection = chosen;

                } else {

                    bool isWeapon = item->FUN_00401170() == 0x28 && item->FUN_004c0bf0();

                    if (chosen->FUN_00418770() > 1 && item->FUN_00401170() != 0x29 && !isWeapon) {

                        selection = new ExtraShell();

                        selection->FUN_00411ec0(chosen);

                        selection->FUN_00419ad0(1);

                        chosen->FUN_00419ad0(chosen->FUN_00418770() - 1);

                        if (chosen->FUN_0042de90() >= 0)

                            chosen->FUN_0042dec0();

                    } else selection = chosen;

                }

                remaining = false;

            } else {

                cursor = cursor->_ref_00726070();

            }

        }

    }

    if (selection) {

        selection->FUN_00419ad0((unsigned short)number);

        remaining = false;

        if (!itemCount->pExtraObjectList)

            itemCount->pExtraObjectList = new ExtraNodeShell();

        if (!((ExtraNodeShell*)itemCount->pExtraObjectList)->FUN_005f65d0(&selection))

            ((ExtraNodeShell*)itemCount->pExtraObjectList)->FUN_005ae3d0(&selection);

        if (result && !(*result)->FUN_005f65d0(&selection))

            (*result)->FUN_005ae3d0(&selection);

        chosen = selection;

    }

    if (remaining) {

        chosen = new ExtraShell();

        if (number > 1)

            chosen->FUN_00419ad0((unsigned short)number);

        if (!itemCount->pExtraObjectList)

            itemCount->pExtraObjectList = new ExtraNodeShell();

        if (!((ExtraNodeShell*)itemCount->pExtraObjectList)->FUN_005f65d0(&chosen))

            ((ExtraNodeShell*)itemCount->pExtraObjectList)->FUN_005ae3d0(&chosen);

        if (result) {

            if (!*result)

                *result = new ExtraNodeShell();

            if (!(*result)->FUN_005f65d0(&chosen))

                (*result)->FUN_005ae3d0(&chosen);

        }

    }

}