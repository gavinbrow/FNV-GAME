struct C90160Matrix {
    float m00, m01, m02;
    float m10, m11, m12;
    float m20, m21, m22;
};
extern const C90160Matrix DAT_011a9448;

class C90160Derived : public BC88760Base {
public:
    C90160Matrix matrix;
    C90160Derived() : matrix(DAT_011a9448) {}
    virtual ~C90160Derived();

    void FUN_00c81580(C90160Derived* destination, BC88760CloningProcess& cloning);
    C90160Derived* FUN_00c90160(BC88760CloningProcess& cloning);
};

C90160Derived* C90160Derived::FUN_00c90160(BC88760CloningProcess& cloning)
{
    BC88760AllocTagScope allocationCategory(16);
    C90160Derived* destination = new C90160Derived;
    FUN_00c81580(destination, cloning);
    destination->matrix = matrix;
    return destination;
}
