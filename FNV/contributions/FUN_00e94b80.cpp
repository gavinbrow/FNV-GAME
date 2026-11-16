#include <d3d9.h>
struct NiMemObject { static void* operator new(unsigned int); };
struct FUN_00e94b00 : NiMemObject {
 int value00,value04,value08,value0c; IDirect3DVertexBuffer9* buffer;
 int unk14,unk18,unk1c,unk20,unk24,unk28,unk2c,unk30;
 FUN_00e94b00() throw();
};
void FUN_00e941a0(void*);
FUN_00e94b00* FUN_00e94b80(int value, IDirect3DVertexBuffer9* buffer, int first, int second, int third) {
 FUN_00e94b00* object=new FUN_00e94b00;
 if(object) {
 object->value0c=value;
 if(buffer) { object->buffer=buffer; buffer->AddRef(); }
 else { if(object->buffer) object->buffer->Release(); object->buffer=0; }
 object->value04=first; object->value08=second; object->value00=third;
 FUN_00e941a0(object);
 }
 return object;
}

