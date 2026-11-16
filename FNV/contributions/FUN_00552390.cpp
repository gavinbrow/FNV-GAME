struct SceneNode {
 unsigned int FUN_0043b480();
 struct SceneChild* FUN_0043b4a0(unsigned int);
};
struct SceneChild {
 bool FUN_00552470();
};
struct SceneController {
 bool FUN_00552490();
 bool FUN_005524b0();
};
struct SceneEntity {
 virtual void UnkVirtual00();
virtual void UnkVirtual01();
virtual void UnkVirtual02();
virtual void UnkVirtual03();
virtual void UnkVirtual04();
virtual void UnkVirtual05();
virtual void UnkVirtual06();
virtual void UnkVirtual07();
virtual void UnkVirtual08();
virtual void UnkVirtual09();
virtual void UnkVirtual0a();
virtual void UnkVirtual0b();
virtual void UnkVirtual0c();
virtual void UnkVirtual0d();
virtual void UnkVirtual0e();
virtual void UnkVirtual0f();
virtual void UnkVirtual10();
virtual void UnkVirtual11();
virtual void UnkVirtual12();
virtual void UnkVirtual13();
virtual void UnkVirtual14();
virtual void UnkVirtual15();
virtual void UnkVirtual16();
virtual void UnkVirtual17();
virtual void UnkVirtual18();
virtual void UnkVirtual19();
virtual void UnkVirtual1a();
virtual void UnkVirtual1b();
virtual void UnkVirtual1c();
virtual void UnkVirtual1d();
virtual void UnkVirtual1e();
virtual void UnkVirtual1f();
virtual void UnkVirtual20();
virtual void UnkVirtual21();
virtual void UnkVirtual22();
virtual void UnkVirtual23();
virtual void UnkVirtual24();
virtual void UnkVirtual25();
virtual void UnkVirtual26();
virtual void UnkVirtual27();
virtual void UnkVirtual28();
virtual void UnkVirtual29();
virtual void UnkVirtual2a();
virtual void UnkVirtual2b();
virtual void UnkVirtual2c();
virtual void UnkVirtual2d();
virtual void UnkVirtual2e();
virtual void UnkVirtual2f();
virtual void UnkVirtual30();
virtual void UnkVirtual31();
virtual void UnkVirtual32();
virtual void UnkVirtual33();
virtual void UnkVirtual34();
virtual void UnkVirtual35();
virtual void UnkVirtual36();
virtual void UnkVirtual37();
virtual void UnkVirtual38();
virtual void UnkVirtual39();
virtual void UnkVirtual3a();
virtual void UnkVirtual3b();
virtual void UnkVirtual3c();
virtual void UnkVirtual3d();
virtual void UnkVirtual3e();
virtual void UnkVirtual3f();
 virtual bool IsEligibleForUpdate();
 void* unk04;
void* unk08;
void* unk0c;
void* unk10;
void* unk14;
void* unk18;
void* unk1c;
void* unk20;
void* unk24;
void* unk28;
void* unk2c;
void* unk30;
void* unk34;
void* unk38;
void* unk3c;
void* unk40;
void* unk44;
void* unk48;
void* unk4c;
void* unk50;
void* unk54;
void* unk58;
void* unk5c;
void* unk60;
void* unk64;
void* unk68;
void* unk6c;
void* unk70;
void* unk74;
void* unk78;
void* unk7c;
void* unk80;
void* unk84;
void* unk88;
void* unk8c;
void* unk90;
void* unk94;
void* unk98;
void* unk9c;
void* unka0;
void* unka4;
void* unka8;
 SceneController* controller;
 bool FUN_00933840();
};
SceneEntity* __cdecl FUN_0056f930(SceneChild*);
void __cdecl FUN_00c6c3d0(SceneChild*,int);
void __cdecl FUN_00552390(SceneNode* root)
{
 for (unsigned int index = 0; index < root->FUN_0043b480(); ++index) {
     SceneChild* child = root->FUN_0043b4a0(index);
     if (child != 0) {
         SceneEntity* entity = FUN_0056f930(child);
         if (entity != 0 && entity->IsEligibleForUpdate()) {
             SceneEntity* candidate = entity;
             if (candidate->controller != 0 &&
                 candidate->controller->FUN_00552490() &&
                 !candidate->controller->FUN_005524b0() &&
                 !child->FUN_00552470() &&
                 !candidate->FUN_00933840()) {
                 FUN_00c6c3d0(child, 2);
             }
         }
     }
 }
}