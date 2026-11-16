struct DispatchItem;
struct DispatchOwner { void FUN_00c91620(bool*, DispatchItem*); };
struct DispatchItem {
    unsigned int unknown00;
    unsigned int unknown04;
    DispatchOwner* owner;
    void FUN_00ca8420(unsigned char, unsigned char, unsigned char);
};
struct Dispatcher {
    unsigned int unknown00;
    unsigned int unknown04;
    unsigned int unknown08;
    unsigned int unknown0c;
    unsigned int unknown10;
    DispatchOwner* owner;
    unsigned int unknown18;
    unsigned int unknown1c;
    unsigned int unknown20;
    unsigned int unknown24;
    unsigned int unknown28;
    unsigned int unknown2c;
    int mode;
    void FUN_00d0b5f0(DispatchItem* item);
};
void Dispatcher::FUN_00d0b5f0(DispatchItem* item)
{
    switch (mode) {
    case 0:
        item->FUN_00ca8420(5, 1, 0);
        break;
    case 1:
        item->FUN_00ca8420(5, 1, 0);
        break;
    case 2:
        if (item->owner == owner) {
            bool success;
            owner->FUN_00c91620(&success, item);
        }
        break;
    }
}
