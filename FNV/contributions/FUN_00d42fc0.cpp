struct Vector4 { float x, y, z, w; };
__declspec(align(16)) struct Matrix43 { Vector4 row0, row1, row2, row3; };
struct FUN_00cb2240_shell { void __thiscall FUN_00cb2240(const Matrix43*, const Matrix43*); };
struct Object { int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c; Matrix43 transform; };
struct Input { Object* object; int unk04; Matrix43* transform; };
struct DispatchData { int unk00; int unk04; Matrix43* unk08; Input* unk0c; };
struct Handler {
    virtual int V0(); virtual int V1(); virtual int V2(); virtual int V3();
    virtual int V4(); virtual int V5(); virtual int V6(); virtual int V7();
    virtual int Dispatch(DispatchData*, int, int, int);
};
struct Owner { int unk00; int unk04; int unk08; Handler* handler; int FUN_00d42fc0(Input*, int, int, int); };
int Owner::FUN_00d42fc0(Input* input, int a, int b, int c)
{
    Object* object = input->object;
    Matrix43 temp;
    ((FUN_00cb2240_shell*)&temp)->FUN_00cb2240(input->transform, &object->transform);
    DispatchData data;
    data.unk08 = &temp;
    data.unk0c = input;
    data.unk00 = object->unk14;
    data.unk04 = 0;
    return handler->Dispatch(&data, a, b, c);
}
