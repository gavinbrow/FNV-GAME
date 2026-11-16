class CB770Facet {
public:
    virtual void v0(int);
    CB770Facet* FUN_00acb770();
};
class Owner {
    int padding;
    CB770Facet* member;
public:
    void FUN_00ec3451();
};
void Owner::FUN_00ec3451() {
    CB770Facet* p = member->FUN_00acb770();
    if (p) p->v0(1);
}
