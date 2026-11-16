#include <xmmintrin.h>
struct BlockData { __m128 position; __m128 rotation; };
struct Command { unsigned char type; void* owner; BlockData* data; };
struct QueueCA8960 { int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c; int unk40; int unk44; int unk48; int unk4c; int unk50; int unk54; int unk58; int unk5c; int unk60; int unk64; int unk68; int unk6c; int unk70; int unk74; int unk78; int unk7c; int unk80; int unk84; int unk88; int unk8c; int unk90; int unk94; void __thiscall FUN_00c91160(Command* cmd); };
struct AllocCA8960 { virtual void v00(); virtual BlockData* Allocate(unsigned int bytes); };
struct FUN_00ca8960_Class { int unk00;int unk04;QueueCA8960* queue08;
 void __thiscall FUN_00ca8860(const __m128* position,const __m128* rotation);
 void FUN_00ca8960(const __m128* position,const __m128* rotation); };
void FUN_00ca8960_Class::FUN_00ca8960(const __m128* position,const __m128* rotation) {
 if(queue08 && queue08->unk94) {
 Command cmd;
 cmd.type=0x18;
 cmd.owner=this;
 FNVTaskMemoryRouter* router=FUN_00c85750();
 cmd.data=((AllocCA8960*)router->allocator)->Allocate(32);
 cmd.data->position=*position;
 cmd.data->rotation=*rotation;
 queue08->FUN_00c91160(&cmd);
 }else FUN_00ca8860(position,rotation);
}