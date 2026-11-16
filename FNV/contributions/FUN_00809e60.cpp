// Adapted from contributor Worker18 (2026-10-23); independently verified and modified.


struct Actor;


void* operator new(unsigned int);


struct Obj12 {


    Obj12();


    ~Obj12();


    int f00, f04, f08;


    void __thiscall FUN_004be930();


    int __thiscall FUN_004459e0(int a);


};


struct Sound {


    virtual void v00();


    virtual void v01();


    virtual void v02();


    virtual void v03();


    virtual void v04();


    virtual void v05();


    virtual void v06();


    virtual void v07();


    virtual void v08();


    virtual void v09();


    virtual void v10();


    virtual void v11();


    virtual void v12();


    virtual void v13();


    virtual void v14();


    virtual void v15();


    virtual void v16();


    virtual void v17();


    virtual void v18();


    virtual void v19();


    virtual void v20();


    virtual void v21();


    virtual void v22();


    virtual void v23();


    virtual void v24();


    virtual void v25();


    virtual void v26();


    virtual void v27();


    virtual void v28();


    virtual void v29();


    virtual void v30();


    virtual void v31();


    virtual void v32();


    virtual void v33();


    virtual void v34();


    virtual void v35();


    virtual void v36();


    virtual void v37();


    virtual void v38();


    virtual void v39();


    virtual void v40();


    virtual void v41();


    virtual void v42();


    virtual void v43();


    virtual void v44();


    virtual void v45();


    virtual void v46();


    virtual void v47();


    virtual void v48();


    virtual void v49();


    virtual void v50();


    virtual void v51();


    virtual void v52();


    virtual void v53();


    virtual void v54();


    virtual void v55();


    virtual void v56();


    virtual void v57();


    virtual void v58();


    virtual void v59();


    virtual void v60();


    virtual void v61();


    virtual void v62();


    virtual void v63();


    virtual void v64();


    virtual void v65();


    virtual void v66();


    virtual void v67();


    virtual void v68();


    virtual void v69();


    virtual void v70();


    virtual void v71();


    virtual void v72();


    virtual void v73();


    virtual void v74();


    virtual void v75();


    virtual int VCall130();


};


struct TESSound {


    void* m_00;


};


struct FUN_008579e0_shell {


    void __thiscall FUN_008579e0(void* buf, unsigned int n);


};


struct TimeGlobal : FUN_008579e0_shell {


    unsigned int __thiscall GetTimeStamp();


};


struct EffectSetting : TimeGlobal {


    TESSound* __thiscall GetBoltSound();


};


struct TESSaveLoadGame : EffectSetting {


    bool __thiscall FUN_00862110();


    unsigned char __thiscall FUN_008df040();


};


extern TESSaveLoadGame* DAT_011de45c;


extern "C" Sound* __cdecl _ref_004839c0(void* a);


void __cdecl FUN_005b5e40(const char* fmt, ...);


int __fastcall FUN_0044ddc0(Obj12* p);


extern char DAT_01015718;


extern char DAT_010156a8;


extern char DAT_01015588;


extern char DAT_01015500;


extern char DAT_010154a0;


extern char DAT_01015440;


extern char DAT_01079810;


struct This {


    int f00, f04, f08, f0c, f10, f14, f18, f1c, f20, f24, f28, f2c, f30, f34, f38, f3c, f40, f44, f48;


    Obj12* m_4c;


    Obj12* m_50[20];


    int fA0;


    unsigned char fA4, fA5, fA6, fA7;


    unsigned char fA8;


    void __thiscall FUN_00806e30(Actor* a);


    void __thiscall FUN_00809e60(Actor* param);


};


void This::FUN_00809e60(Actor* param)


{


    FUN_00806e30(param);


    unsigned short w18 = 0;


    int flag = 0;


    if (DAT_011de45c->FUN_00862110()) {


        unsigned int i;


        DAT_011de45c->FUN_008579e0(&i, 4);


        if (i != 0x424c4f4b) {


            TESSound* rec = DAT_011de45c->GetBoltSound();


            if (rec != 0) {


                Sound* pForm;


                pForm = _ref_004839c0(rec->m_00);


                FUN_005b5e40(&DAT_01015718, &DAT_01079810, 0x2da, rec->m_00, pForm->VCall130(), *(unsigned char*)((char*)rec + 9), *(int*)((char*)rec + 5));


            } else {


                FUN_005b5e40(&DAT_010156a8, &DAT_01079810, 0x2da, DAT_011de45c->FUN_008df040());


            }


        }


        flag = DAT_011de45c->GetTimeStamp();


        DAT_011de45c->FUN_008579e0(&w18, 2);


    }


    unsigned char n1c;


    DAT_011de45c->FUN_008579e0(&n1c, 1);


    if (n1c) {


        m_4c = new Obj12;


        m_4c->FUN_004be930();


    }


    int rec2 = 0;


    for (; rec2 < 0x14; rec2++) {


        DAT_011de45c->FUN_008579e0(&n1c, 1);


        if (n1c) {


        m_50[rec2] = new Obj12;


        m_50[rec2]->FUN_004be930();


        if (!FUN_0044ddc0(m_50[rec2])) {
           delete m_50[rec2];
           m_50[rec2] = 0;
        }


        }


    }


    fA4 = 1;


    if ((int)DAT_011de45c->FUN_008df040() >= 0x41) {


        DAT_011de45c->FUN_008579e0(&fA0, 4);


        DAT_011de45c->FUN_008579e0(&fA4, 1);


    }


    if ((int)DAT_011de45c->FUN_008df040() >= 0x6b) {


        DAT_011de45c->FUN_008579e0(&fA8, 1);


    }


    if (DAT_011de45c->FUN_00862110()) {


        unsigned int ts;


        ts = DAT_011de45c->GetTimeStamp();


        TESSound* tag = DAT_011de45c->GetBoltSound();


        if (tag != 0) {


            Sound* snd2 = _ref_004839c0(tag->m_00);


            if ((unsigned int)ts > (unsigned int)w18 + (unsigned int)flag) {


                FUN_005b5e40(&DAT_01015588, (int)((unsigned int)ts - ((unsigned int)w18 + (unsigned int)flag)), &DAT_01079810, 0x302, tag->m_00, snd2->VCall130(), *(unsigned char*)((char*)tag + 9), *(int*)((char*)tag + 5));


            } else if ((unsigned int)ts < (unsigned int)w18 + (unsigned int)flag) {


                FUN_005b5e40(&DAT_01015500, (int)(((unsigned int)w18 + (unsigned int)flag) - (unsigned int)ts), &DAT_01079810, 0x302, tag->m_00, snd2->VCall130(), *(unsigned char*)((char*)tag + 9), *(int*)((char*)tag + 5));


            }


        } else {


            if ((unsigned int)ts > (unsigned int)w18 + (unsigned int)flag) {


                FUN_005b5e40(&DAT_010154a0, (int)((unsigned int)ts - ((unsigned int)w18 + (unsigned int)flag)), &DAT_01079810, 0x302, DAT_011de45c->FUN_008df040());


            } else if ((unsigned int)ts < (unsigned int)w18 + (unsigned int)flag) {


                FUN_005b5e40(&DAT_01015440, (int)(((unsigned int)w18 + (unsigned int)flag) - (unsigned int)ts), &DAT_01079810, 0x302, DAT_011de45c->FUN_008df040());


            }


        }


    }


}


