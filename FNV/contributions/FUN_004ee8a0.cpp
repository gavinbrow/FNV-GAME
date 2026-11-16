struct DecalListNode {
    void* vtable;
    DecalListNode* next;
    ~DecalListNode();
};
struct DecalListManager {
    int unk00;
    DecalListNode* head;
    void FUN_006e5cc0(DecalListNode* node);
    void FUN_0066b0d0(int state);
    void FUN_004ee8a0();
};
void DecalListManager::FUN_004ee8a0() {
    if (head != 0) {
        DecalListNode* node = head;
        head = node->next;
        FUN_006e5cc0(node);
        node->next = 0;
        delete node;
    } else {
        FUN_0066b0d0(0);
    }
}