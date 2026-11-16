struct CollisionNode { int unk00; int unk04; unsigned char* status; };
struct CollisionState {
    int unk00; int unk04; int unk08; int unk0C;
    CollisionNode* node;
    bool FUN_00c659a0();
};
bool CollisionState::FUN_00c659a0() {
    if (node) {
        unsigned char* status = node->status;
        unsigned int kind = status ? status[0xE8] : 4;
        return kind == 4 || kind == 5;
    }
    return false;
}