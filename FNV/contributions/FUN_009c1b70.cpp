

struct Vec3 { float x,y,z; };

struct Ref {

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

virtual void slot11();

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

virtual bool IsActor();

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

virtual void ApplyTime(float, int);

virtual void slot82();

virtual void slot83();

virtual void slot84();

virtual void slot85();

virtual void slot86();

virtual void slot87();

virtual void slot88();

virtual void ApplyValue(int);

virtual int GetValue();

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

virtual void slot116();

virtual void slot117();

virtual void slot118();

virtual void slot119();

virtual void slot120();

virtual void slot121();

virtual void slot122();

virtual void slot123();

virtual void slot124();

virtual void slot125();

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

virtual bool CheckFlag(int);

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

virtual void slot194();

virtual void slot195();

virtual void slot196();

virtual void slot197();

virtual void slot198();

virtual void slot199();

virtual void slot200();

virtual void slot201();

virtual void slot202();

virtual void slot203();

virtual void slot204();

virtual void slot205();

virtual void slot206();

virtual void slot207();

virtual void slot208();

virtual void slot209();

virtual void slot210();

virtual void slot211();

virtual void slot212();

virtual void slot213();

virtual void slot214();

virtual void slot215();

virtual bool IsValidTarget();

    int FUN_0043fcd0();

    bool FUN_00437b90();

    bool FUN_00477ba0();

    unsigned int FUN_0044ddc0();

    unsigned short FUN_00645c20();

    int FUN_00517630();

    int FUN_00963eb0(int,float,int);

    void FUN_0089a760(void*,int);

};

struct Hit {

    Ref* reference;

    Vec3 position;

    Vec3 normal;

    int itemID;

    int unk20;

    int unk24;

    bool valid28;

    bool valid29;

};

struct HitList {

    Hit* data;

    HitList* next;

    bool FUN_008256d0();

    Hit** FUN_006815c0();

    HitList* FUN_00726070();

};

struct ContactHelper {
    void* reference;

    ContactHelper(void*);

    ~ContactHelper();

    Ref* FUN_00559450();

};

struct LoadedProjectile {
int unk00;
int unk04;
int unk08;
int unk0c;
int unk10;
int unk14;
int unk18;
int unk1c;
int unk20;
int unk24;
int unk28;
int unk2c;
int unk30;
int unk34;
int unk38;
int unk3c;
int unk40;
int unk44;
int unk48;
int unk4c;
int unk50;
int unk54;
int unk58;
int unk5c;
int unk60;

    LoadedProjectile();

    ~LoadedProjectile();

};

struct Resource {

    int FUN_0043fcd0();

    int FUN_00517630();

};

struct EventStatus {

    bool FUN_004fd360();

    bool FUN_00975300();

    bool FUN_005de080();

};

extern Ref* DAT_011dea3c;

extern Ref* DAT_011f21e8;

extern Ref* DAT_011f21ec;

extern float DAT_0102918c;

extern double DAT_01012060;

struct TargetSettings { bool FUN_00525430(); };
extern TargetSettings DAT_011f2250;

extern void __cdecl FUN_0082ee10();

extern Ref* __cdecl FUN_004b5a80(int);

struct FormID { Ref* FUN_00460140(); };

extern LoadedProjectile* __cdecl FUN_009b4d90();

extern void __cdecl FUN_009b5650(Ref*,int,Ref*,int,Ref*);



struct ImpactProjectile : Ref {

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

    HitList list88;

    bool impacted90;

    bool FUN_009c1b70();

    float FUN_00885d70();

    Ref* FUN_00874480();

    Ref* FUN_00476c90();

    EventStatus* FUN_004181e0();

    void FUN_009c30d0(Ref*,int);

    void FUN_009c20e0(Ref*,const Vec3*,const Vec3*,Ref*,int);

    Vec3 FUN_009b7010(Ref*);

    void FUN_009c2e80(Vec3,Vec3);

};

bool ImpactProjectile::FUN_009c1b70() {

    bool processed=false;

    bool inverse=false;

    if(!impacted90 && !list88.FUN_008256d0()) {

        HitList* node=&list88;

        while(node && !node->FUN_008256d0()) {

            Hit* hit=*node->FUN_006815c0();

            node=node->FUN_00726070();

            bool aChanged=false;

            Ref* aTarget=hit->reference;

            if(aTarget && FUN_00885d70() > DAT_01012060 && hit->valid29) {

                int oldState = hit->reference->FUN_0043fcd0();

                if(FUN_00874480() && FUN_00874480()->IsActor() &&

                   aTarget->IsActor() && !FUN_00874480()->FUN_00437b90()) {

                    inverse=!aTarget->CheckFlag(0);

                    FUN_009c30d0(aTarget,0);

                } else {

                    Ref* form=FUN_004b5a80(hit->itemID);

                    if(form && form->FUN_00517630()<4)

                        aTarget->ApplyValue(GetValue());

                    Ref* attacker = (FUN_00874480() && FUN_00874480()->IsActor()) ? FUN_00874480() : 0;

                    float jump=0.0f;

                    if(attacker && attacker->IsValidTarget() && DAT_011f2250.FUN_00525430() && FUN_00476c90())

                        jump=(float)FUN_00476c90()->FUN_00645c20();

                    float delay=FUN_00885d70()+jump;

                    if(aTarget->IsActor()) {

                        Ref* actor=aTarget;
                        ContactHelper helper(new LoadedProjectile());

                        FUN_009b5650(helper.FUN_00559450(),0,actor,0,this);

                        inverse=!actor->CheckFlag(0);

                        actor->FUN_0089a760(helper.FUN_00559450(),0);

                    } else {

                        hit->reference->ApplyTime(delay,0);

                    }

                    if(aTarget->FUN_00477ba0() && FUN_00874480() == DAT_011dea3c)

                        DAT_011dea3c->FUN_00963eb0(10,DAT_0102918c,0);

                }

                if(oldState!=aTarget->FUN_0043fcd0()) aChanged=true;

            }

            if(!aTarget || !(aTarget->FUN_0044ddc0() & 0x20)) {

                if(!FUN_004181e0()->FUN_004fd360() || FUN_004181e0()->FUN_00975300() || FUN_004181e0()->FUN_005de080()) {

                    if(!aChanged) {

                        if(DAT_011f21e8 && DAT_011f21e8==FUN_00874480() && aTarget && aTarget->IsActor())

                            FUN_0082ee10();

                        if(DAT_011f21ec && DAT_011f21ec==FUN_00874480() && aTarget && aTarget->IsActor() && aTarget->CheckFlag(0) && inverse)

                            FUN_0082ee10();

                        Ref* form=hit->itemID ? ((FormID*)hit->itemID)->FUN_00460140() : 0;

                        FUN_009c20e0(aTarget,&hit->position,&hit->normal,form,hit->unk20);

                        FUN_009c2e80(hit->position,FUN_009b7010(form));

                    }

                }

            }

            processed=true;

            if(FUN_00437b90())

                break;

        }

        impacted90=true;

    }

    return processed;

}

