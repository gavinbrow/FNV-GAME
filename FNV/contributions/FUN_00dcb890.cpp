extern int DAT_010d73fc;
extern int DAT_010d62f4;
void* FUN_00c85750();
struct FUN_00dcb890_Owner { int unk00; int unk04; int unk08; };
struct FUN_00dcb890_Node { void* key; int next; };
struct FUN_00dcb890_Table {
    FUN_00dcb890_Node* m_nodes;
    int FUN_00dc8e30(int key);
    void FUN_00dcb4b0(int key, int idx);
};
struct FUN_00dcb890_Ref {
    virtual void Destroy(int flags);
    virtual FUN_00dcb890_Owner* Lookup();
    int unk04;
    int refCount;
};
struct FUN_00dcb890_Pair { int key; FUN_00dcb890_Ref* ref; };
struct FUN_00dcb890_Alloc {
    virtual void s0();
    virtual void s1();
    virtual void s2();
    virtual void s3();
    virtual void Free(void* p, int size);
};
struct FUN_00dcb890_Holder {
    int unk00; int unk04; int unk08; int unk0c;
    FUN_00dcb890_Alloc* m10;
};
struct FUN_00dcb890_cls {
    void* unk00; int unk04; int unk08;
    FUN_00dcb890_Pair* unk0c;
    int unk10; int unk14;
    FUN_00dcb890_Ref* unk18;
    void FUN_00dcb890();
};
void FUN_00dcb890_cls::FUN_00dcb890()
{
    unk00 = &DAT_010d73fc;
    for (int i = 0; i < unk10; ++i) {
        FUN_00dcb890_Ref* r = unk0c[i].ref;
        if (--r->refCount == 0)
            r->Destroy(1);
    }
    int base = unk18->Lookup()->unk08;
    int key = ((int (__thiscall*)(FUN_00dcb890_cls*))((void**)unk00)[6])(this);
    FUN_00dcb890_Table* tbl = reinterpret_cast<FUN_00dcb890_Table*>(base + 0x6c);
    int idx = tbl->FUN_00dc8e30(key);
    if (idx != -1) {
        FUN_00dcb890_Node* nodes = tbl->m_nodes;
        do {
            if ((void*)this == nodes[idx].key) {
                tbl->FUN_00dcb4b0(key, idx);
                break;
            }
            idx = nodes[idx].next;
        } while (idx != -1);
    }
    FUN_00dcb890_Ref* ref = unk18;
    if (ref) {
        if (--ref->refCount == 0)
            ref->Destroy(1);
    }
    unk18 = 0;
    FUN_00dcb890_Holder* h = (FUN_00dcb890_Holder*)FUN_00c85750();
    FUN_00dcb890_Alloc* a = h->m10;
    int cap = unk14;
    unk10 = 0;
    if (!(cap & 0x80000000))
        a->Free(unk0c, (cap & 0x3fffffff) * 8);
    unk0c = 0;
    int& flag = unk14;
    flag = (int)0x80000000;
    unk00 = &DAT_010d62f4;
}