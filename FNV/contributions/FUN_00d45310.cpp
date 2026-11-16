struct FUN_00d45310_target {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual void v4();
    virtual void v5();
    virtual void v6();
    virtual void v7();
    virtual void v8();
    virtual void v9();
    virtual void v10();
    virtual void v11();
    virtual void v12(int value);
};
struct FUN_00d45310_owner {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00d45310_target* unk10;
    void FUN_00d45310(int value);
};
void FUN_00d45310_owner::FUN_00d45310(int value) {
    if (unk10)
        unk10->v12(value);
}
