struct Builder {
    void FUN_00a4c4b0(BSFadeNode*, unsigned int);
    BSFadeNode* FUN_00a4c5e0(unsigned int);
};
BSFadeNode* Builder::FUN_00a4c5e0(unsigned int flags) {
    BSFadeNode* allocated = static_cast<BSFadeNode*>(BSFadeNode::operator new(0x44));
    BSFadeNode* node = allocated ? static_cast<BSFadeNode*>(allocated->FUN_00a4bcf0(0, 0, 0)) : 0;
    FUN_00a4c4b0(node, flags);
    return node;
}