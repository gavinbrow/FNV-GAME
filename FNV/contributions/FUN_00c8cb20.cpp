#include <intrin.h>
struct StrArr {void* unk00; char** data; unsigned short capacity,size,live,growBy; void FUN_0096ad30(unsigned int); void FUN_0096ae90(unsigned int,char*const&); void append(char*const& text) {unsigned int index=size; if(index>=capacity) FUN_0096ad30(index+growBy); FUN_0096ae90(index,text);} };
struct NiPoint3 {float x,y,z; char* FUN_00a59af0(const char*);};
struct NiTransform {float rotation[9]; NiPoint3 translate; float scale; char* FUN_00a598f0(const char*);};
struct NativeTransform {float rotation[12]; float translation[4];};
void __cdecl FUN_00624b10(NiTransform*,NiPoint3*);
void __cdecl FUN_00458620(NiPoint3*,const float*);
extern NativeTransform DAT_01268370;
char* __cdecl FUN_00a7d330(void*);
extern unsigned int DAT_0126fd98;
extern __declspec(thread) unsigned int currentTask;
struct AutoMemContext {unsigned int ePreviousContext;
 AutoMemContext() { ePreviousContext=currentTask; currentTask=16; }
 ~AutoMemContext() {currentTask=ePreviousContext;}
};
struct Component {
virtual void v00();
virtual void v04();
virtual void v08();
virtual void v0c();
virtual void v10();
virtual void v14();
virtual void v18();
virtual void v1c();
virtual void v20();
virtual void v24();
virtual void v28();
virtual void v2c();
virtual void v30();
virtual void v34();
virtual void v38();
virtual void v3c();
virtual void v40();
virtual void v44();
virtual void v48();
virtual void v4c();
virtual void v50();
virtual void v54();
virtual void v58();
virtual void v5c();
virtual void serialize(StrArr*);
};
struct Holder {unsigned int unk00,unk04; Component* component;};
struct State {unsigned int unk00,unk04,unk08,unk0c,unk10; Holder* holder; unsigned int unk18,unk1c,unk20,unk24,unk28,unk2c; NativeTransform world;};
struct Object {unsigned int unk00,unk04; State* state; void FUN_00c851c0(StrArr*); void FUN_00c8cb20(StrArr*);
 Component* getComponent() {
  if(this) {
   State* current=state;
   if(current) {
    Holder* holder=current->holder;
    if(!holder) return 0;
    return holder->component;
   }
   return 0;
  }
  return 0;
 }
};
void Object::FUN_00c8cb20(StrArr* output) {
 AutoMemContext task;
 FUN_00c851c0(output);
 output->append(FUN_00a7d330(*(void**)&g_012681b4));
 const NativeTransform* world=this && state ? &state->world:&DAT_01268370;
 NiTransform transform;
 FUN_00624b10(&transform,(NiPoint3*)world);
 FUN_00458620(&transform.translate,world->translation);
 output->append(transform.translate.FUN_00a59af0("Trans"));
 output->append(transform.FUN_00a598f0("Rot"));
 Component* component=getComponent();
 if(component) component->serialize(output);
}


