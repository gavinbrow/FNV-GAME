struct Setting {float* FUN_00403e20();};extern Setting DAT_011d1890,DAT_011d1bd4,DAT_011d19f0;
struct RTTI {};extern RTTI DAT_012024e0,DAT_01202550,DAT_01202540;
struct Object {virtual void method0();virtual void method1();virtual void method2();virtual void* AsNode();};
bool FUN_0043b300(const RTTI*,Object*);void* FUN_00653270(const RTTI*,Object*);
struct Emitter {float FUN_00759450();void FUN_00819a70(float);};
struct Controller {float FUN_00639aa0();void FUN_0098adb0(float);float FUN_004a7bd0();void FUN_00819a50(float);float FUN_00792760();void FUN_00444020(float);};
struct Particle:Object {unsigned FUN_004d7d50();Object* FUN_004d7d70(unsigned);};
struct Node:Object {unsigned FUN_0043b480();Object* FUN_0043b4a0(unsigned);};
struct Effect {int unk0;int unk4;int unk8;int unkC;int unk10;int unk14;int unk18;int unk1C;int unk20;int unk24;int unk28;int unk2C;int unk30;int unk34;int unk38;int unk3C;int unk40;int unk44;int unk48;int unk4C;int unk50;int unk54;int unk58;int unk5C;int unk60;int unk64;int unk68;int unk6C;int unk70;int unk74;int unk78;int unk7C;int unk80;int unk84;int unk88;int unk8C;int unk90;int unk94;int unk98;int unk9C;int unkA0;int unkA4;int unkA8;float sizeScale,speedScale;void FUN_00819890(Object*);};
void Effect::FUN_00819890(Object* object)
{
 float scale2;
 {float scale3;
  {float scale1=sizeScale**DAT_011d1890.FUN_00403e20();
   scale2=speedScale**DAT_011d1bd4.FUN_00403e20();
   scale3=speedScale**DAT_011d19f0.FUN_00403e20();
   if(FUN_0043b300(&DAT_012024e0,object)) {
    Particle* particle=(Particle*)object;
    for(unsigned i=0;i<particle->FUN_004d7d50();++i) {
     Controller* controller;
     {Emitter* emitter;
      {Object* entry=particle->FUN_004d7d70(i);
     emitter=(Emitter*)FUN_00653270(&DAT_01202550,entry);
     if(emitter)emitter->FUN_00819a70(emitter->FUN_00759450()*scale1);
     controller=(Controller*)FUN_00653270(&DAT_01202540,entry);
     if(controller) {
      controller->FUN_0098adb0(controller->FUN_00639aa0()*scale1);
      controller->FUN_00819a50(controller->FUN_004a7bd0()*scale3);
      controller->FUN_00444020(controller->FUN_00792760()*scale2);
     } } }
    }
   } else if(object && object->AsNode()) {
    Node* node=(Node*)object;
    for(unsigned i=0;i<node->FUN_0043b480();++i) {
     Object* child=node->FUN_0043b4a0(i);
     FUN_00819890(child);
    }
   }
  }
 }
}

