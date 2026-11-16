struct __declspec(align(16)) FNVTransform {
    float m[16];
    void FUN_00cb2240(const FNVTransform* parent, const FNVTransform* local);
};
class FUN_00df66a0_Node {
public:
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3(FNVTransform* dest);
    virtual void v4();
    virtual void v5();
    virtual void v6();
    virtual void v7();
    virtual FUN_00df66a0_Node* v8();
    void FUN_00df66a0(FNVTransform* dest);
};
void FUN_00df66a0_Node::FUN_00df66a0(FNVTransform* dest) {
    if (v8()) {
        FNVTransform parent;
        FNVTransform local;
        v8()->FUN_00df66a0(&parent);
        v3(&local);
        dest->FUN_00cb2240(&parent,&local);
    } else {
        v3(dest);
    }
}