struct Base {
    int unk04;
    Base() throw();
    virtual void vf();
};

struct Node : Base {
    int unk08[14];
    static void* operator new(unsigned int size) throw();
    Node() throw() {}
    virtual void vf();
};

struct Owner {
    void FUN_00c32de0(Node* node, int arg);
    Node* FUN_00c2b160(int arg);
};

Node* Owner::FUN_00c2b160(int arg)
{
    Node* node = new Node();
    FUN_00c32de0(node, arg);
    return node;
}
