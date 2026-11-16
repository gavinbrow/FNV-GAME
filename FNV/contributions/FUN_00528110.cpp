
struct FUN_005287e0_Class {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual void v4();
    virtual void v5();
    unsigned char FUN_005287e0();
};
struct Query {
    void* vtbl; int m_a; int m_b; char m_c;
    Query();
    ~Query();
    unsigned char FUN_006ebde0();
};
struct Handle {
    FUN_005287e0_Class* value;
    Handle(int);
    ~Handle();
    FUN_005287e0_Class* FUN_00559450();
};
struct Controller {
    unsigned char FUN_00906570(Query*, unsigned int*, Handle*, unsigned int);
    void FUN_00528110();
};
void Controller::FUN_00528110() {
    Query query;
    while (!query.FUN_006ebde0()) {
        unsigned int x = 0;
        Handle y(0);
        if (FUN_00906570(&query, &x, &y, 1)) {
            if (y.FUN_00559450()->FUN_005287e0()) {
                y.FUN_00559450()->v5();
            }
        }
    }
}