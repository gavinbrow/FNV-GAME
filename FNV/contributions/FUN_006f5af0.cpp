struct Scene {};
struct Node {virtual void method0();virtual void method1();virtual void method2();virtual void method3();virtual void method4();virtual void method5();virtual void method6();virtual void method7();virtual void method8();virtual void method9();virtual void method10();virtual void method11();virtual void method12();virtual void method13();virtual void method14();virtual void method15();virtual void method16();virtual void method17();virtual void method18();virtual void method19();virtual void method20();virtual void method21();virtual void method22();virtual void method23();virtual void method24();virtual void method25();virtual void method26();virtual void method27();virtual void method28();virtual void method29();virtual void method30();virtual void method31();virtual void method32();virtual void method33();virtual void method34();virtual void method35();virtual void method36();virtual void method37();virtual void method38();virtual void method39();virtual void method40();virtual void method41();virtual void method42();virtual void method43();virtual void method44();virtual void method45();virtual void method46();virtual void method47();virtual void method48();virtual void method49();virtual void method50();virtual void method51();virtual void method52();virtual void method53();virtual void method54();virtual void method55();virtual void method56();virtual void method57();virtual void Detach(Scene*);};
struct Parent {Node* FUN_004ea9c0();};
struct ParentRef {Parent* value;Parent* FUN_00559450();};
struct SceneRef {Scene* value;Scene* FUN_00559450();void FUN_0066b0d0(Scene*);};
struct TaskRef {void* value;void FUN_006f74f0(void*);};
extern int DAT_011d8510;
struct Block {ParentRef* parent;SceneRef first,second,third,fourth,fifth;TaskRef mainTask,secondaryTask;int unk20;bool active;void FUN_006f60c0();void FUN_006f5af0();};
void Block::FUN_006f5af0()
{
 FUN_006f60c0();
 if(second.FUN_00559450() || first.FUN_00559450() || fourth.FUN_00559450())--DAT_011d8510;
 if(second.FUN_00559450() || first.FUN_00559450()) {
  parent->FUN_00559450()->FUN_004ea9c0()->Detach(second.FUN_00559450());
  parent->FUN_00559450()->FUN_004ea9c0()->Detach(first.FUN_00559450());
  parent->FUN_00559450()->FUN_004ea9c0()->Detach(third.FUN_00559450());
  second.FUN_0066b0d0(0);first.FUN_0066b0d0(0);third.FUN_0066b0d0(0);mainTask.FUN_006f74f0(0);
 }
 if(fourth.FUN_00559450()) {
  parent->FUN_00559450()->FUN_004ea9c0()->Detach(fourth.FUN_00559450());
  fourth.FUN_0066b0d0(0);fifth.FUN_0066b0d0(0);secondaryTask.FUN_006f74f0(0);
 }
 active=false;
}
