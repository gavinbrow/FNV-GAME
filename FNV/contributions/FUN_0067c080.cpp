struct FUN_00670b30_Object {
    ~FUN_00670b30_Object();
};
struct FUN_0067ad70_Base {
    virtual void v0();
    ~FUN_0067ad70_Base();
};
struct FUN_0067c080 : FUN_0067ad70_Base {
    FUN_00670b30_Object* ownedObject;
    ~FUN_0067c080();
};
FUN_0067c080::~FUN_0067c080()
{
    delete ownedObject;
}