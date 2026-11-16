



struct Vec3 { float x, y, z; float FUN_00457990(); };



struct OutHandle { int value; OutHandle(const OutHandle&); int FUN_004a3a20(); };



struct GameObject {



    virtual void slot0();



    virtual void slot1();



    virtual void slot2();



    virtual void slot3();



    virtual void slot4();



    virtual void slot5();



    virtual void slot6();



    virtual void slot7();



    virtual void slot8();



    virtual void slot9();



    virtual void slot10();



    virtual GameObject* child();



    virtual void slot12();



    virtual void slot13();



    virtual void slot14();



    virtual void slot15();



    virtual void slot16();



    virtual void slot17();



    virtual void slot18();



    virtual void slot19();



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



    virtual void slot50();



    virtual void slot51();



    virtual void slot52();



    virtual void slot53();



    virtual void slot54();



    virtual void slot55();



    virtual void slot56();



    virtual void slot57();



    virtual void slot58();



    virtual void slot59();



    virtual void slot60();



    virtual void slot61();



    virtual void slot62();



    virtual void slot63();



    virtual bool isSpecial();



    virtual void slot65();



    virtual void slot66();



    virtual void slot67();



    virtual void slot68();



    virtual void slot69();



    virtual void slot70();



    virtual void slot71();



    virtual void slot72();



    virtual void slot73();



    virtual void slot74();



    virtual void slot75();



    virtual void slot76();



    virtual void slot77();



    virtual void slot78();



    virtual void slot79();



    virtual void slot80();



    virtual void slot81();



    virtual void slot82();



    virtual void slot83();



    virtual void slot84();



    virtual void slot85();



    virtual void slot86();



    virtual void slot87();



    virtual void slot88();



    virtual void slot89();



    virtual void slot90();



    virtual void slot91();



    virtual void slot92();



    virtual void slot93();



    virtual void slot94();



    virtual void slot95();



    virtual void slot96();



    virtual void slot97();



    virtual void slot98();



    virtual void slot99();



    virtual void slot100();



    virtual void slot101();



    virtual void slot102();



    virtual void slot103();



    virtual void slot104();



    virtual void slot105();



    virtual void slot106();



    virtual void slot107();



    virtual void slot108();



    virtual void slot109();



    virtual void slot110();



    virtual void slot111();



    virtual void slot112();



    virtual void slot113();



    virtual void slot114();



    virtual void slot115();



    virtual int formID();



    virtual void slot117();



    virtual void slot118();



    virtual void slot119();



    virtual void slot120();



    virtual void slot121();



    virtual void slot122();



    virtual void slot123();



    virtual void slot124();



    virtual Vec3* position();



    virtual void slot126();



    virtual void slot127();



    virtual void slot128();



    virtual void slot129();



    virtual void slot130();



    virtual void slot131();



    virtual void slot132();



    virtual void slot133();



    virtual void slot134();



    virtual void slot135();



    virtual void slot136();



    virtual void slot137();



    virtual void slot138();



    virtual void slot139();



    virtual void slot140();



    virtual void slot141();



    virtual void slot142();



    virtual void slot143();



    virtual void slot144();



    virtual void slot145();



    virtual void slot146();



    virtual void slot147();



    virtual void slot148();



    virtual void slot149();



    virtual void slot150();



    virtual void slot151();



    virtual void slot152();



    virtual void slot153();



    virtual void slot154();



    virtual void slot155();



    virtual void slot156();



    virtual void slot157();



    virtual void slot158();



    virtual void slot159();



    virtual void slot160();



    virtual void slot161();



    virtual void slot162();



    virtual void slot163();



    virtual void slot164();



    virtual void slot165();



    virtual void slot166();



    virtual void slot167();



    virtual void slot168();



    virtual void slot169();



    virtual void slot170();



    virtual void slot171();



    virtual void slot172();



    virtual void slot173();



    virtual void slot174();



    virtual void slot175();



    virtual void slot176();



    virtual void slot177();



    virtual void slot178();



    virtual void slot179();



    virtual void slot180();



    virtual void slot181();



    virtual void slot182();



    virtual void slot183();



    virtual void slot184();



    virtual void slot185();



    virtual void slot186();



    virtual void slot187();



    virtual void slot188();



    virtual void slot189();



    virtual void slot190();



    virtual void slot191();



    virtual void slot192();



    virtual void slot193();



    virtual void visitReference(GameObject*,int);



    OutHandle FUN_00931ed0();



    OutHandle FUN_0043b4f0();



    GameObject* FUN_006fa820();



    int FUN_004a3a20();



    float FUN_00457990();



    GameObject* FUN_0045bb80(Vec3*, void*);



    GameObject* FUN_00439ef0();



    void FUN_00440460(void*);



    void FUN_004f0160(void*);



    void FUN_0043fa80(void*);



    void FUN_00bc28b0(float, float, float, bool);



    bool FUN_00ee8990();



};



struct Holder { GameObject* FUN_00559450(); };



struct Pending {



    Vec3 FUN_00439ef0(Vec3*);



    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18;



    float value1c;



    struct RefList* refs20;



};



struct RefList { unsigned short count; unsigned short reserved; int entries[1]; };



struct LocalStore {



    void* value;



    void FUN_004a39f0(int);



    void FUN_0059ce80(int);



    void FUN_00810f90(int);



};



struct Control {



    void FUN_0070c440(LocalStore*);



    void FUN_00810ff0(void*);



};



struct Matrix {



    float a,b,c,d,e,f,g,h,i;



    void FUN_006815c0();



    void FUN_00a59780(float,float,float);



};



struct Clock { float* FUN_00403e20(); };



extern Clock DAT_011d1758;



extern GameObject* DAT_011dea3c;



extern GameObject* __cdecl FUN_004b5260(int);



extern int __cdecl FUN_005dbe10();



extern void __cdecl FUN_0080fae0(float);



extern GameObject* __cdecl FUN_00825550(int);



extern void __cdecl Deallocate(void*);



extern float __cdecl FUN_004b5550(float,float);



struct Root : GameObject {



    int unk004;



    int unk008;



    int unk00c;



    int unk010;



    int unk014;



    int unk018;



    int unk01c;



    int unk020;



    int unk024;



    int unk028;



    int unk02c;



    int unk030;



    int unk034;



    int unk038;



    int unk03c;



    int unk040;



    int unk044;



    int unk048;



    int unk04c;



    int unk050;



    int unk054;



    int unk058;



    int unk05c;



    int unk060;



    int unk064;



    int unk068;



    int unk06c;



    int unk070;



    int unk074;



    int unk078;



    int unk07c;



    int unk080;



    int unk084;



    float f088;



    int unk08c;



    int unk090;



    int unk094;



    int unk098;



    int unk09c;



    int unk0a0;



    int unk0a4;



    Holder m0a8;



    int state0ac;



    Pending* active0b0;



    Holder m0b4;



    int unk0b8;



    Holder m0bc;



    void FUN_00932520(int,int);



    Control* FUN_009306d0();



    GameObject* FUN_009185e0();



    void FUN_008133d0(int);



    void FUN_00814d40(int,int);



};



void Root::FUN_00814d40(int arg1, int arg2)



{



    FUN_00932520(arg1,arg2);



    Control* a = FUN_009306d0();
LocalStore handle;



    if(a) {



        int selected;



        if(FUN_009185e0() && FUN_009185e0()->child()) {



            GameObject* special = FUN_009185e0()->child();



            GameObject* current = special->isSpecial() ? special : 0;



            if(current) {



                



                selected = current->FUN_00931ed0().FUN_004a3a20();



            } else {



                GameObject* form = FUN_004b5260(special->formID());



                GameObject* item = form ? form->FUN_006fa820() : 0;



                selected = item ? item->FUN_0043b4f0().FUN_004a3a20() : FUN_005dbe10();



            }



        } else {



            GameObject* form = FUN_004b5260(formID());



            GameObject* item = form ? form->FUN_006fa820() : 0;



            selected = item ? item->FUN_0043b4f0().FUN_004a3a20() : FUN_005dbe10();



        }



        a->FUN_0070c440(&handle);



        handle.FUN_004a39f0(7);



        handle.FUN_0059ce80(selected);



        a->FUN_00810ff0(handle.value);



    }



    GameObject* candidate = FUN_009185e0() ? FUN_009185e0()->child() : 0;



    if(candidate != DAT_011dea3c) {



        FUN_0080fae0(*DAT_011d1758.FUN_00403e20());



    }



    Pending* pending = active0b0;



    if(pending) {



        if(m0b4.FUN_00559450()) {



            m0b4.FUN_00559450()->FUN_00440460(pending);



            m0b4.FUN_00559450()->FUN_004f0160(&pending->unk0c);



            bool force = state0ac != 0;



            if(m0bc.FUN_00559450()) {



                Vec3 position3d;



                m0bc.FUN_00559450()->FUN_0045bb80(&position3d,pending)->FUN_00439ef0();



                m0a8.FUN_00559450()->FUN_00bc28b0(pending->value1c,position3d.FUN_00457990(),f088,force);



                Matrix rot;



                rot.FUN_006815c0();



                float angle=position3d.z;



                position3d.z=0.0f;



                float azimuth = position3d.FUN_00457990();




                rot.FUN_00a59780(FUN_004b5550(position3d.x,position3d.y),0.0f,-FUN_004b5550(angle,azimuth));



                m0b4.FUN_00559450()->FUN_0043fa80(&rot);



            } else {



                Vec3 position3d = *this->position();




                float direction = pending->FUN_00439ef0(&position3d).FUN_00457990();



                m0a8.FUN_00559450()->FUN_00bc28b0(pending->value1c,direction,f088,force);



                if(m0a8.FUN_00559450()->FUN_00ee8990() || state0ac==2) {



                    FUN_008133d0(2);



                    LocalStore handle;



                    FUN_009306d0()->FUN_0070c440(&handle);



                    handle.FUN_00810f90(1);



                    FUN_009306d0()->FUN_00810ff0(handle.value);
}




                }



        }



        active0b0=0;



        if(pending->refs20) {



            unsigned short count=pending->refs20->count;



            for(unsigned int i=0;i<count;++i) {



                GameObject* ref;
{
int id=pending->refs20->entries[i];
ref=FUN_00825550(id);
}



                if(ref) visitReference(ref,0);



            }



        }



        delete pending;



    }



}



