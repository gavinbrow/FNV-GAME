struct BSFadeNode {
    static void* __cdecl operator new(unsigned int size);
    BSFadeNode* __thiscall FUN_00c1b5c0();
};
struct CloneSource {
    void __thiscall FUN_00c1b6f0(BSFadeNode*, unsigned int);
    BSFadeNode* __thiscall FUN_00c1b9e0(unsigned int);
};
BSFadeNode* CloneSource::FUN_00c1b9e0(unsigned int flags) {
    void* memory = BSFadeNode::operator new(0x110);
    BSFadeNode* node;
    if (memory)
        node = ((BSFadeNode*)memory)->FUN_00c1b5c0();
    else
        node = 0;
    FUN_00c1b6f0(node, flags);
    return node;
}
