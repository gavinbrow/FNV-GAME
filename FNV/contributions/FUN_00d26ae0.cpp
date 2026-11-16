struct CallbackShape {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0c();
    virtual void v10();
    virtual void v14();
    virtual void v18();
    virtual void v1c(void* first, float value, void* last);
};
struct ShapeDispatch {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    CallbackShape* shape;
    void FUN_00d26ae0(void* first, float value, void* last);
};
void ShapeDispatch::FUN_00d26ae0(void* first, float value, void* last) {
    shape->v1c(first, value, last);
}
