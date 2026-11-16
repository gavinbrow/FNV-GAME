struct Node { bool __thiscall FUN_00a01230(int property); Node* __thiscall FUN_00a011f0(int property); Node* __thiscall FUN_0045cd60(); void __thiscall FUN_00a011b0(int property); void __thiscall FUN_00700320(int property, int value); };
extern int __cdecl FUN_0044a670(Node* node); extern int __cdecl FUN_00ec62c0();
struct Menu0076ab40 {
unsigned int unk000;
unsigned int unk004;
unsigned int unk008;
unsigned int unk00c;
unsigned int unk010;
unsigned int unk014;
unsigned int unk018;
unsigned int unk01c;
unsigned int unk020;
unsigned int unk024;
unsigned int unk028;
unsigned int unk02c;
unsigned int unk030;
unsigned int unk034;
unsigned int unk038;
unsigned int unk03c;
unsigned int unk040;
unsigned int unk044;
unsigned int unk048;
unsigned int unk04c;
unsigned int unk050;
unsigned int unk054;
unsigned int unk058;
unsigned int unk05c;
unsigned int unk060;
unsigned int unk064;
unsigned int unk068;
unsigned int unk06c;
unsigned int unk070;
unsigned int unk074;
unsigned int unk078;
unsigned int unk07c;
unsigned int unk080;
unsigned int unk084;
unsigned int unk088;
unsigned int unk08c;
unsigned int unk090;
unsigned int unk094;
unsigned int unk098;
unsigned int unk09c;
unsigned int unk0a0;
unsigned int unk0a4;
unsigned int unk0a8;
unsigned int unk0ac;
unsigned int unk0b0;
unsigned int unk0b4;
unsigned int unk0b8;
unsigned int unk0bc;
unsigned int unk0c0;
unsigned int unk0c4;
unsigned int unk0c8;
unsigned int unk0cc;
unsigned int unk0d0;
unsigned int unk0d4;
unsigned int unk0d8;
unsigned int unk0dc;
unsigned int unk0e0;
unsigned int unk0e4;
unsigned int unk0e8;
unsigned int unk0ec;
unsigned int unk0f0;
unsigned int unk0f4;
unsigned int unk0f8;
unsigned int unk0fc;
unsigned int unk100;
unsigned int unk104;
unsigned int unk108;
unsigned int unk10c;
unsigned int unk110;
unsigned int unk114;
unsigned int unk118;
Node* active; Node* root; void __thiscall FUN_0076ab40();
};
void Menu0076ab40::FUN_0076ab40() {
    Node* selected;
    int total;
    {
        int multiplier = 0;
        total = 0;
        if (root->FUN_00a01230(0xfa3)) {
            selected = root->FUN_00a011f0(0xfc4);
            if (selected) multiplier = FUN_0044a670(selected);
        }
        for (Node* current = root; current && current != active->FUN_0045cd60(); current = current->FUN_0045cd60()) {
            current->FUN_00a011b0(0xfa1);
            total += FUN_00ec62c0();
        }
        active->FUN_00700320(0xfa1, multiplier * 17 + total);
    }
}