struct Form { int FUN_00401170(); };
struct Node {
    int unk00, unk04, unk08, unk0c, unk10, unk14;
    int payload18;
    Node* FUN_00726070();
};
struct Target { void FUN_00824110(void* data); };
struct Virtual {
    virtual void vf00(); virtual void vf04(); virtual void vf08();
    virtual void vf0c(); virtual void vf10();
    virtual void vf14(void* data, int obj, int val);
};
extern char DAT_01183108;
extern char DAT_011839b4;
extern "C" void* __cdecl FUN_00ec43fb(void*, int, const void*, const void*, int);
struct Obj {
    int unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c,unk20,unk24,
        unk28,unk2c,unk30,unk34,unk38,unk3c,unk40,unk44,unk48,unk4c,
        unk50,unk54,unk58,unk5c,unk60,unk64,unk68,unk6c,unk70,unk74,
        unk78,unk7c,unk80,unk84;
    Virtual unk88;
    int unk8c, unk90;
    Target unk94;
    void FUN_0095ea30(Form* form, int unused);
};
void Obj::FUN_0095ea30(Form* form, int unused) {
    if (form->FUN_00401170() != 24 && form->FUN_00401170() != 26)
        return;
    Node* result = static_cast<Node*>(FUN_00ec43fb(form, 0, &DAT_01183108, &DAT_011839b4, 0));
    Node* node = result ? result->FUN_00726070() : 0;
    if (node) {
        unk88.vf14(node ? &node->payload18 : 0, (int)form, 0);
        unk94.FUN_00824110(node ? &node->payload18 : 0);
    }
}