struct Vector4 { float x,y,z,w; };
__declspec(align(16)) struct Matrix43 { Vector4 row0,row1,row2,row3; };
struct MatrixOps { void FUN_00cb2240(const Matrix43*, const Matrix43*); };
struct Object { int unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c,unk20,unk24,unk28,unk2c; Matrix43 transform; };
struct Input { Object* object; int unk04; Matrix43* transform; };
struct DispatchData { int unk00; int unk04; Matrix43* unk08; Input* unk0c; };
struct Handler { virtual int V0(); virtual int V1(); virtual int V2(); virtual int Dispatch(DispatchData*,int,int,int); };
struct Owner { int a,b,c; Handler* handler; void FUN_00d42ed0(Input*,int,int,int); };
void Owner::FUN_00d42ed0(Input* input,int a,int b,int c)
{
    Object* object=input->object;
    Matrix43 temp;
    ((MatrixOps*)&temp)->FUN_00cb2240(input->transform,&object->transform);
    DispatchData data;
    data.unk08=&temp;
    data.unk0c=input;
    data.unk00=object->unk14;
    data.unk04=0;
    handler->Dispatch(&data,a,b,c);
}
