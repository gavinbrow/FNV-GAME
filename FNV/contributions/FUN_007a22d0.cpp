struct Item {
    int* data;
    int key;
};
struct Node {
    Item** __thiscall FUN_006815c0();
    Node* __thiscall FUN_00726070();
};
struct Owner {
    int unk00;
    Node head;
    int* __thiscall FUN_007a22d0(int* key);
};
int* Owner::FUN_007a22d0(int* key) {
    Node* iter = this ? &head : 0;
    for (; iter && *iter->FUN_006815c0(); iter = iter->FUN_00726070()) {
        if ((*iter->FUN_006815c0())->key == *key) {
            return (*iter->FUN_006815c0())->data;
        }
    }
    return 0;
}