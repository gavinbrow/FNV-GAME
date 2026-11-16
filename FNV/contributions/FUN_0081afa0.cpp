void* __cdecl operator new(unsigned int);
struct Form {};
struct FUN_0081aa80 {Form* form;unsigned char flags;FUN_0081aa80* next;FUN_0081aa80(Form*,unsigned char,FUN_0081aa80*);};
struct SaveManager {void FUN_008579e0(void*,unsigned);unsigned char FUN_008df040();};extern SaveManager* DAT_011de45c;
void* __cdecl FUN_00401460(void*,const void*,unsigned);
struct Projectile {virtual void method0();virtual void method1();virtual void method2();virtual void method3();virtual void method4();virtual void method5();virtual void method6();virtual void method7();virtual void method8();virtual void method9();virtual void method10();virtual void method11();virtual void method12();virtual void method13();virtual void method14();virtual void method15();virtual void method16();virtual void method17();virtual void method18();virtual void method19();virtual void method20();virtual void method21();virtual void method22();virtual void method23();virtual void method24();virtual void method25();virtual void method26();virtual void method27();virtual void method28();virtual void method29();virtual void method30();virtual void method31();virtual void method32();virtual void method33();virtual void method34();virtual void method35();virtual void method36();virtual void method37();virtual void method38();virtual void method39();virtual void method40();virtual void method41();virtual void method42();virtual void method43();virtual void method44();virtual void method45();virtual void method46();virtual void method47();virtual void method48();virtual void method49();virtual void method50();virtual void method51();virtual void method52();virtual void method53();virtual void method54();virtual void method55();virtual void method56();virtual void method57();virtual void method58();virtual void method59();virtual void method60();virtual void method61();virtual void method62();virtual void method63();virtual void method64();virtual void method65();virtual void method66();virtual void method67();virtual void method68();virtual void method69();virtual void method70();virtual void method71();virtual void method72();virtual void method73();virtual void method74();virtual void method75();virtual void method76();virtual void method77();virtual void method78();virtual void method79();virtual void method80();virtual void method81();virtual void method82();virtual void method83();virtual void method84();virtual void method85();virtual void method86();virtual void method87();virtual void method88();virtual void method89();virtual void method90();virtual void method91();virtual void method92();virtual void method93();virtual void method94();virtual void method95();virtual void method96();virtual void method97();virtual void method98();virtual void method99();virtual void method100();virtual void method101();virtual void method102();virtual void method103();virtual void method104();virtual void method105();virtual void method106();virtual void method107();virtual void method108();virtual void method109();virtual void method110();virtual void method111();virtual void method112();virtual void Reset();int unk4;int unk8;int unkC;int unk10;int unk14;int unk18;int unk1C;int unk20;int unk24;int unk28;int unk2C;int unk30;int unk34;int unk38;int unk3C;int unk40;int unk44;int unk48;int unk4C;int unk50;int unk54;int unk58;int unk5C;int unk60;int unk64;int unk68;int unk6C;int unk70;int unk74;int unk78;int unk7C;int unk80;int unk84;int unk88;int unk8C;int unk90;int unk94;int unk98;int unk9C;int unkA0;int unkA4;int unkA8;int unkAC;int unkB0;int unkB4;int unkB8;int unkBC;int unkC0;int unkC4;FUN_0081aa80* head;unsigned id;void FUN_00819830();void FUN_0081e980(int,int);void FUN_00484d00(void*,unsigned);void FUN_00484d40(void*,unsigned);void FUN_0081afa0(int,int);};
void Projectile::FUN_0081afa0(int a,int b)
{
 FUN_00819830();Reset();FUN_0081e980(a,b);
 FUN_00484d00(&unkA8,4);FUN_00484d00(&unk88,4);FUN_00484d00(&unkAC,4);
 DAT_011de45c->FUN_008579e0(&unkB4,4);FUN_00484d00(&unkB8,4);
 if(unkB4==1){unsigned formID;FUN_00484d00(&formID,4);FUN_00401460(&id,&formID,4);}
 if(DAT_011de45c->FUN_008df040()>=0x71) {
  FUN_00484d00(&unkB0,4);unsigned short count;FUN_00484d00(&count,2);
  for(unsigned i=0;i<count;++i) {
   FUN_0081aa80* record;
   {Form* form; {unsigned char flags;
    FUN_00484d40(&form,4);FUN_00484d00(&flags,1);
    record=new FUN_0081aa80(form,flags,head);
    head=record; }
   }
  }
 }
}


