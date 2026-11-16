struct CombatWorldState {
    int FUN_00559450();
    unsigned int FUN_00726070();
};
struct WorldStateNode {
    CombatWorldState*& FUN_006815c0();
    WorldStateNode* FUN_0062d990();
    bool FUN_009aa410(int type, unsigned int* output);
};
bool WorldStateNode::FUN_009aa410(int type, unsigned int* output) {
    WorldStateNode* current = this;
    while (current != 0) {
        CombatWorldState* state = current->FUN_006815c0();
        if (state != 0 && state->FUN_00559450() == type) {
            *output = state->FUN_00726070();
            return true;
        }
        current = current->FUN_0062d990();
    }
    return false;
}