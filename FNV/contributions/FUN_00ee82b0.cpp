#include <windows.h>
struct Ref { virtual void slot0() = 0; virtual void slot1() = 0; };
struct Item { virtual ~Item(); };
extern int DAT_0109b944;
struct Obj {
    virtual void baseSlot() = 0;
    int pad04; int pad08; int pad0c; int pad10; int pad14; int pad18; int pad1c; int pad20;
    Item* item24; int pad28; int pad2c; Ref* ref30;
    int pad34; int pad38; int pad3c; int pad40; int pad44; int pad48;
    Ref* ref4c; Ref* ref50; Ref* ref54; Ref* ref58; Ref* ref5c; Ref* ref60; Ref* end64;
    void FUN_00ee82b0(); void FUN_00a5f800(); void FUN_00a5c240();
};
void Obj::FUN_00ee82b0()
{
    Ref** next = &end64;
    int count = 5;
    do {
        Ref* p = *--next;
        if (p && InterlockedDecrement((volatile long*)p + 1) == 0)
            p->slot1();
        --count;
    } while (count >= 0);
    Ref* p = ref30;
    if (p && InterlockedDecrement((volatile long*)p + 1) == 0)
        p->slot1();
    *(int*)this = (int)&DAT_0109b944;
    if (item24)
        delete item24;
    FUN_00a5f800();
    FUN_00a5c240();
}

