struct Node1;
struct Node2;
struct Node3;
struct Node4;
struct Node5;
struct Node0 { Node1* FUN_007af430(); };
struct Node1 { Node2* FUN_0051cba0(int); };
struct Node2 { Node3* FUN_0043b4a0(int); };
struct Node3 {
    Node4* FUN_005495f0();
    Node5* FUN_00a59d30(int);
};
struct Node4 {
    void FUN_00a67050(int);
    void FUN_004410d0(int);
    void FUN_004410f0(int);
};
struct Node5 {
    int FUN_00441110();
    void FUN_00441130(int, int);
};
void __cdecl FUN_00b57e30(Node3*, int, int);
struct Owner {
    virtual void vfn_00();
    virtual void vfn_04();
    virtual void vfn_08();
    virtual void vfn_0c();
    virtual void vfn_10();
    virtual void vfn_14();
    virtual void vfn_18();
    virtual void vfn_1c();
    virtual void vfn_20();
    virtual void vfn_24();
    virtual void vfn_28();
    virtual void vfn_2c();
    virtual void vfn_30();
    virtual void vfn_34(Node2*);
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    Node0* unk28;
    void FUN_00440fd0();
};
void Owner::FUN_00440fd0()
{
    Node1* node1 = unk28->FUN_007af430();
    Node2* node2 = node1->FUN_0051cba0(0);
    if (node2) {
        Node3* node3 = node2->FUN_0043b4a0(0);
        Node4* status = node3->FUN_005495f0();
        status->FUN_00a67050(0x4000);
        status->FUN_004410d0(0x11);
        status->FUN_004410f0(1);
        FUN_00b57e30(node3, 0, 0);
        Node5* action = (node3->FUN_00a59d30(3) == 0 ? false : node3->FUN_00a59d30(3)->FUN_00441110() == 0xb) ? node3->FUN_00a59d30(3) : 0;
        if (action) {
            action->FUN_00441130(13, 1);
            action->FUN_00441130(22, 1);
        }
        vfn_34(node2);
    }
}