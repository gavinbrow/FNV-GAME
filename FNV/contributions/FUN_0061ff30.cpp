struct NodeBase0 {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
};
struct NodeBase16 {
    NodeBase16* __thiscall FUN_006207a0(NodeBase16* previous);
};
struct Node : NodeBase0, NodeBase16 {};
struct Holder {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    Node* node14;
    void __thiscall FUN_0061ff30(Node* node);
};
void FUN_0087e9b0(int value);

void Holder::FUN_0061ff30(Node* node)
{
    if (node == 0)
        return;
    node14 = static_cast<Node*>(node->FUN_006207a0(node14));
    Node* toRelease = node;
    FUN_0087e9b0((int)toRelease);
}
