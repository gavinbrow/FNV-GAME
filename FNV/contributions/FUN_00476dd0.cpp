extern unsigned char DAT_01202e84;
struct NodeChildren;
struct Node {
    virtual void Unknown0();
    virtual void Unknown1();
    virtual void Unknown2();
    virtual NodeChildren* GetChildren();
    unsigned char FUN_00c455a0(unsigned char mode);
    int FUN_0045bb80(void* extra, float value);
};
struct NodeChildren {
    unsigned int FUN_0043b480();
    Node* FUN_0043b4a0(unsigned int index);
};
struct Context {
    float FUN_00567400();
    int FUN_008d6f30(int value);
};
struct Receiver {
    void FUN_004fa6f0(int value);
};
extern unsigned char __cdecl FUN_0043b300(const void* descriptor, Node* node);
struct Walk {
    int FUN_00476dd0(Node* node, Receiver* receiver, unsigned int mode, Context* context, void* extra);
};
int Walk::FUN_00476dd0(Node* node, Receiver* receiver, unsigned int mode, Context* context, void* extra)
{
    if (node == 0)
        return 0;
    int count = 0;
    if (FUN_0043b300(&DAT_01202e84, node)) {
        Node* typed = node;
        if (typed->FUN_00c455a0((unsigned char)mode)) {
            receiver->FUN_004fa6f0(context->FUN_008d6f30(typed->FUN_0045bb80(extra, context->FUN_00567400())));
            count++;
        }
    }
    NodeChildren* children = node->GetChildren();
    if (children != 0) {
        for (unsigned int index = 0; index < children->FUN_0043b480(); ++index) {
            count += FUN_00476dd0(children->FUN_0043b4a0(index), receiver, mode, context, extra);
        }
    }
    return count;
}