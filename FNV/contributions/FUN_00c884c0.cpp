struct FNVTransformState {
    int component00, component04, component08, component0c;
    int component10, component14, component18, component1c;
    int component20, component24, component28, component2c;
    int component30;
};

struct FNVTraversalNode {
    int unknown00, unknown04, unknown08, unknown0c;
    int unknown10, unknown14;
    FNVTraversalNode* parent;
    int unknown1c, unknown20, unknown24;
    int unknown28, unknown2c, unknown30;
    FNVTransformState state;
};

struct FNVTraversalOutput : FNVTransformState {
    void FUN_00a86bf0();
    FNVTransformState FUN_0062c250(FNVTransformState* state);
};

void __cdecl FUN_00c884c0(FNVTraversalNode* node,
                          FNVTraversalNode* stop,
                          FNVTraversalOutput* output)
{
    if (node == 0)
        return;
    if (node == stop) {
        output->FUN_00a86bf0();
        return;
    }
    FUN_00c884c0(node->parent, stop, output);
    static_cast<FNVTransformState&>(*output) = output->FUN_0062c250(&node->state);
}