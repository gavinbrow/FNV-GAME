struct CopyNpc;

struct CopyComponent {int tag;void FUN_0048cce0(CopyComponent*);void FUN_00481c80(CopyComponent*);void FUN_004870f0(CopyComponent*);void FUN_0047fb50(CopyComponent*);void FUN_004786e0(CopyComponent*);void FUN_00480000(CopyComponent*);void FUN_00487240(CopyComponent*);void FUN_0048d630(CopyComponent*);void FUN_0047bdd0(CopyComponent*);void FUN_0047f1e0(CopyComponent*);void FUN_0047f2d0(CopyComponent*);void FUN_006ecd40(int);int FUN_00726070();};

struct CopyPrefix {

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

    virtual void slot64();

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

    virtual bool GetFemale();

    virtual void SetFemale(bool);

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

    virtual void* GetStyle();

    virtual void SetStyle(void*);    int unk004;

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



    int FUN_00401170();

};

struct CopyData {

    virtual void slot0();

    virtual void slot1();

    virtual void slot2();

    virtual void slot3();

    virtual void Reset(int);

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

    virtual unsigned int GetValue();

    virtual void SetValue(unsigned int);

    virtual unsigned short GetStat();

    virtual float GetFactor();

    virtual int GetData();    int unk004;

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

    CopyComponent container;

    int unk038;

    int unk03c;

    CopyComponent touch;

    int unk044;

    int unk048;

    CopyComponent spell;

    int unk050;

    int unk054;

    int unk058;

    int unk05c;

    CopyComponent ai;

    int unk064;

    int unk068;

    int unk06c;

    int unk070;

    int unk074;

    int unk078;

    int unk07c;

    CopyComponent health;

    int unk084;

    CopyComponent attributes;

    int unk08c;

    int unk090;

    CopyComponent animation;

    int unk098;

    int unk09c;

    CopyComponent fullName;

    int unk0a4;

    int unk0a8;

    int unk0ac;

    int unk0b0;

    int unk0b4;

    int unk0b8;

    int unk0bc;

    int unk0c0;

    CopyComponent model;

    int unk0c8;

    int unk0cc;

    int unk0d0;

    CopyComponent destructible;

    int unk0d8;

    CopyComponent race;

    int unk0e0;

    unsigned char skills[14];unsigned char skillOffsets[14];



    void FUN_00604ba0(CopyPrefix*);

    CopyNpc* FUN_0059bb30();bool FUN_0047cdd0();bool FUN_0047cca0();bool FUN_0047cd40(int);unsigned int* FUN_00717e50();void FUN_0047dd30(unsigned int);int FUN_00441110();void FUN_0050f9a0(int);void FUN_0050f9c0(int);bool FUN_00461580(bool,bool);void FUN_0047dd50(bool,bool);void FUN_0047e1c0(float);unsigned short FUN_0047d3d0();void FUN_0047dea0(unsigned short);unsigned short FUN_0047d370();void FUN_0047dfe0(unsigned short);bool FUN_00461560();void FUN_005d1070(bool);unsigned short FUN_0047d390();void FUN_0047de40(unsigned short);unsigned short FUN_0047d3b0();void FUN_0047de70(unsigned short);unsigned short FUN_008f21d0();void FUN_0047e270(unsigned short);void FUN_0047e010(unsigned short);void FUN_0047ca20(CopyData*);void FUN_007037c0(CopyNpc*);void FUN_0047cd90(unsigned short);void FUN_0047ccc0(bool);

};

struct CopyNpc:public CopyPrefix,public CopyData {

    void FUN_0050eaa0(CopyNpc*);void FUN_00603790(CopyNpc*);void FUN_00601c70(int);float FUN_00944300();void FUN_009442e0(float);float FUN_00604250();void FUN_006053f0(float);int FUN_00502430();void FUN_00603be0(int);

};

struct DefaultNpcValue {int* FUN_006815c0();};

struct DefaultNpcManager {DefaultNpcValue* FUN_004ea950();DefaultNpcValue* FUN_006130e0();};

extern DefaultNpcManager* DAT_011c3f2c;

void FUN_00401460(void*,const void*,unsigned int);

CopyNpc* FUN_0047d1a0(CopyNpc*,unsigned short*);

void CopyData::FUN_00604ba0(CopyPrefix* argument) {

    CopyNpc* source9;CopyNpc* templateForm;

    {unsigned short flags;

    if(!FUN_0059bb30() && !argument) return;

    {

    TESNPC fallback;

    source9=0;

    if(!FUN_0047cdd0()) source9=FUN_0059bb30();

    if(argument && argument->FUN_00401170()==42) source9=static_cast<CopyNpc*>(argument);

    if(!source9) {

        source9=reinterpret_cast<CopyNpc*>(&fallback);

        source9->race.FUN_006ecd40(*DAT_011c3f2c->FUN_004ea950()->FUN_006815c0());

        source9->FUN_00601c70(*DAT_011c3f2c->FUN_006130e0()->FUN_006815c0());

    } else if(source9->FUN_0059bb30() && !source9->FUN_0047cca0()) source9->Reset(0);

    if(FUN_0047cd40(9)) model.FUN_0048cce0(source9?&source9->model:0);

    if(FUN_0047cd40(8)) container.FUN_00481c80(source9?&source9->container:0);

    if(FUN_0047cd40(7)) {

        fullName.FUN_004870f0(source9?&source9->fullName:0);

        unsigned int ownFlags=*FUN_00717e50();ownFlags&=0xef9f5df5;

        unsigned int sourceFlags4=*source9->FUN_00717e50();sourceFlags4&=0x1060a20a;

        FUN_0047dd30(sourceFlags4|ownFlags);

    }

    if(FUN_0047cd40(6)) {

        animation.FUN_0047fb50(source9?&source9->animation:0);

        reinterpret_cast<CopyNpc*>(reinterpret_cast<char*>(this)-sizeof(CopyPrefix))->FUN_0050eaa0(source9);

        reinterpret_cast<CopyNpc*>(reinterpret_cast<char*>(this)-sizeof(CopyPrefix))->SetValue(source9->GetValue());

        reinterpret_cast<CopyNpc*>(reinterpret_cast<char*>(this)-sizeof(CopyPrefix))->FUN_00603790(source9);

        destructible.FUN_004786e0(source9?&source9->destructible:0);

    }

    if(FUN_0047cd40(0)) {

        FUN_0050f9a0(source9->FUN_00441110());

        FUN_0050f9c0(source9->GetData());

        FUN_0047dd50(true,source9->FUN_00461580(true,true));

        race.FUN_006ecd40(source9->race.FUN_00726070());

        reinterpret_cast<CopyNpc*>(reinterpret_cast<char*>(this)-sizeof(CopyPrefix))->FUN_009442e0(source9->FUN_00944300());

        reinterpret_cast<CopyNpc*>(reinterpret_cast<char*>(this)-sizeof(CopyPrefix))->FUN_006053f0(source9->FUN_00604250());

        reinterpret_cast<CopyNpc*>(reinterpret_cast<char*>(this)-sizeof(CopyPrefix))->FUN_00601c70(source9->FUN_00502430());

        FUN_0047e1c0(source9->GetFactor());

        FUN_0047dea0(FUN_0047d3d0());

        reinterpret_cast<CopyNpc*>(reinterpret_cast<char*>(this)-sizeof(CopyPrefix))->SetStyle(source9->GetStyle());

    }

    if(FUN_0047cd40(1)) {

        FUN_0047dfe0(source9->FUN_0047d370());

        FUN_005d1070(source9->FUN_00461560());

        FUN_0047de40(source9->FUN_0047d390());

        FUN_0047de70(source9->FUN_0047d3b0());

        attributes.FUN_00480000(source9?&source9->attributes:0);

        health.FUN_00487240(source9?&source9->health:0);

        FUN_0047e270(source9->FUN_008f21d0());

        FUN_0047e010(source9->GetStat());

        FUN_00401460(skills,source9->skills,14);

        FUN_00401460(skillOffsets,source9->skillOffsets,14);

        if(FUN_00461560()) reinterpret_cast<CopyNpc*>(reinterpret_cast<char*>(this)-sizeof(CopyPrefix))->SetFemale(true);

        else reinterpret_cast<CopyNpc*>(reinterpret_cast<char*>(this)-sizeof(CopyPrefix))->SetFemale(source9->GetFemale());

    }

    if(FUN_0047cd40(2)) FUN_0047ca20(source9);

    if(FUN_0047cd40(3)) {

        spell.FUN_0048d630(source9?&source9->spell:0);

        touch.FUN_0047bdd0(source9?&source9->touch:0);

    }

    if(FUN_0047cd40(4)) ai.FUN_0047f1e0(source9?&source9->ai:0);

    if(FUN_0047cd40(5)) ai.FUN_0047f2d0(source9?&source9->ai:0);

    if(reinterpret_cast<CopyNpc*>(reinterpret_cast<char*>(this)-sizeof(CopyPrefix))->GetFemale()) reinterpret_cast<CopyNpc*>(reinterpret_cast<char*>(this)-sizeof(CopyPrefix))->FUN_00603be0(0);

    flags=0;

    templateForm=FUN_0047d1a0(reinterpret_cast<CopyNpc*>(reinterpret_cast<char*>(this)-sizeof(CopyPrefix)),&flags);

    if(templateForm) {FUN_007037c0(templateForm);FUN_0047cd90(flags);}

    FUN_0047ccc0(true);

    }

    }}

