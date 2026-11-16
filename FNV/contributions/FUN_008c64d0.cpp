class TESForm;class TESPackage;
TESForm* __cdecl FUN_004839c0(unsigned int id);
struct Manager {virtual void slot00();
virtual void slot01();
virtual void slot02();
virtual void slot03();
virtual void slot04();
virtual void slot05();
virtual void slot06();
virtual void slot07();
virtual void slot08();
virtual void slot09();
virtual void slot0a();
virtual void slot0b();
virtual void slot0c();
virtual void slot0d();
virtual void slot0e();
virtual void slot0f();
virtual void slot10();
virtual void slot11();
virtual void slot12();
virtual void slot13();
virtual void slot14();
virtual void slot15();
virtual void slot16();
virtual void slot17();
virtual void slot18();
virtual void slot19();
virtual void slot1a();
virtual void slot1b();
virtual void slot1c();
virtual void slot1d();
virtual void slot1e();
virtual void slot1f();
virtual void slot20();
virtual void slot21();
virtual void slot22();
virtual void slot23();
virtual void slot24();
virtual void slot25();
virtual void slot26();
virtual void slot27();
virtual void slot28();
virtual void slot29();
virtual void slot2a();
virtual void slot2b();
virtual void slot2c();
virtual void slot2d();
virtual void slot2e();
virtual void slot2f();
virtual void slot30();
virtual void slot31();
virtual void slot32();
virtual void slot33();
virtual void slot34();
virtual void slot35();
virtual void slot36();
virtual void slot37();
virtual void slot38();
virtual void slot39();
virtual void slot3a();
virtual void slot3b();
virtual void slot3c();
virtual void slot3d();
virtual void slot3e();
virtual void slot3f();
virtual void slot40();
virtual void slot41();
virtual void slot42();
virtual void slot43();
virtual void slot44();
virtual void slot45();
virtual void slot46();
virtual void slot47();
virtual void slot48();
virtual void slot49();
virtual void slot4a();
virtual void slot4b();
virtual void slot4c();
virtual void slot4d();
virtual void slot4e();
virtual void slot4f();
virtual void slot50();
virtual void slot51();
virtual void slot52();
virtual void slot53();
virtual void slot54();
virtual void slot55();
virtual void dispatch(); unsigned FUN_0084e3a0();int FUN_009611e0();};
struct Handler{bool FUN_00469860(unsigned);};
extern Handler* DAT_011c3f2c;
int __cdecl FUN_0096a820(int);
struct Owner{Manager* manager;int unk04,unk08,interval;void FUN_008c6080(TESPackage*,int);void FUN_008c64d0(unsigned,unsigned);};
void Owner::FUN_008c64d0(unsigned a,unsigned b){
 if(manager){
  if(a&0){
   if(a&0){
    Manager* saved=manager;
    FUN_008c6080(dynamic_cast<TESPackage*>(FUN_004839c0((unsigned)saved)),0);
   }else{
    if(DAT_011c3f2c->FUN_00469860(manager->FUN_0084e3a0()))manager->dispatch();
   }
  }
  if(manager){
   int elapsed=FUN_0096a820(manager->FUN_009611e0());
   if(interval>=elapsed)interval=elapsed-1;
  }
 }
}
