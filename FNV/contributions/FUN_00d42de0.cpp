struct Matrix4 {
    float values[16];
    void __thiscall FUN_00cb2240(int value, const float* source);
};
struct Owner {
    int m00,m04,m08,m0c,m10;
    int sourceValue;
    int m18,m1c,m20,m24,m28,m2c;
    float matrix[16];
};
struct Input {
    Owner* owner;
    int m04;
    int initValue;
};
struct Params {
    int sourceValue;
    int zero;
    Matrix4* matrix;
    Input* source;
};
struct Dispatcher {
    virtual void v00();
    virtual void v04();
    virtual void v08();
    virtual void v0c();
    virtual void v10(Params *params,int arg2,int arg3,int arg4);
};
struct Controller {
    int m00,m04,m08;
    Dispatcher* dispatcher;
    void FUN_00d42de0(Input* input,int arg2,int arg3,int arg4);
};
void Controller::FUN_00d42de0(Input* input,int arg2,int arg3,int arg4) {
    __declspec(align(16)) Matrix4 matrix;
    Owner* owner = input->owner;
    matrix.FUN_00cb2240(input->initValue, owner->matrix);
    Params params;
    params.matrix=&matrix;
    params.source=input;
    params.sourceValue=owner->sourceValue;
    params.zero=0;
    dispatcher->v10(&params,arg2,arg3,arg4);
}