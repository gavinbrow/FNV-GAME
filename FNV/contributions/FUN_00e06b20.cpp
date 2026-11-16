struct Node {
    Node* next;
    int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34;
    char unk38;
    char unk39;
};
void __stdcall FUN_00e06b20(Node* node) {
    while (node) {
        if (node->unk39) return;
        node->unk39 = 1;
        node = node->next;
    }
}
