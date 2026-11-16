#include <windows.h>

struct Obj {
    virtual void slot0();
    virtual void slot1();
    long unk04;
    void IncRef() { InterlockedIncrement(&unk04); }
    void DecRef() {
        if (InterlockedDecrement(&unk04) == 0)
            slot1();
    }
};

struct Ptr {
    Obj* m;
    Ptr& operator=(const Ptr& rhs) {
        if (m != rhs.m) {
            if (m)
                m->DecRef();
            m = rhs.m;
            if (m)
                m->IncRef();
        }
        return *this;
    }
};

struct Node {
    Node* unk00;
    Node* unk04;
    Ptr unk08;
};

struct Anchor {
    Node* unk00;
    Node* unk04;
};

struct Pool {
    int unk00;
    Node* __thiscall FUN_0043a010();
};

struct Self {
    Node* unk00;
    int unk04;
    Pool unk08;
    Node* __thiscall FUN_00c1b520(Anchor* anchor, Ptr& ref);
};

Node* __thiscall Self::FUN_00c1b520(Anchor* anchor, Ptr& ref)
{
    Node* node = unk08.FUN_0043a010();
    node->unk08 = ref;
    node->unk00 = (Node*)anchor;
    node->unk04 = anchor->unk04;
    if (anchor->unk04)
        anchor->unk04->unk00 = node;
    else
        unk00 = node;
    anchor->unk04 = node;
    ++unk08.unk00;
    return node;
}
