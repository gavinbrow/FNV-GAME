// Reconstruction based on another contributor's 2026-10-24 unverified checkpoint.
extern void* DAT_011dea10;
struct TextureData { unsigned int FUN_007d6bb0(); };
class NiFixedString { public: const char* value; operator const char*() const; };
class NiTexture {
public:
    virtual void v0();
    virtual void v1();
    virtual NiPointer<NiTexture>* v2();
    virtual void v3();
    virtual void v4();
    virtual void v5();
    virtual void v6();
    virtual void v7();
    virtual void v8();
    virtual void v9();
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
    virtual char* v37();
    virtual char* v38();
    virtual NiFixedString* v39();
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
    virtual const char* v76();
    NiFixedString* FUN_00413f40();
    TextureData* FUN_0059bb30();
    int FUN_0043c430();
    int FUN_00726070();
    NiTexture* FUN_0055b980();
};
template<> class NiPointer<NiTexture> {
public:
    NiTexture* object;
    NiPointer();
    ~NiPointer();
    operator NiTexture*() const;
    NiPointer& operator=(const NiPointer&);
    NiPointer& operator=(NiTexture*);
};
class BSFile {
public:
    char internalbuf16[16];
    unsigned int unk014;
    unsigned int unk018;
    unsigned int unk01c;
    unsigned int unk020;
    unsigned int unk024;
    unsigned int unk028;
    unsigned int unk02c;
    unsigned int unk030;
    unsigned int unk034;
    unsigned int unk038;
    unsigned int unk03c;
    unsigned int unk040;
    unsigned int unk044;
    unsigned int unk048;
    unsigned int unk04c;
    unsigned int unk050;
    unsigned int unk054;
    unsigned int unk058;
    unsigned int unk05c;
    unsigned int unk060;
    unsigned int unk064;
    unsigned int unk068;
    unsigned int unk06c;
    unsigned int unk070;
    unsigned int unk074;
    unsigned int unk078;
    unsigned int unk07c;
    unsigned int unk080;
    unsigned int unk084;
    unsigned int unk088;
    unsigned int unk08c;
    unsigned int unk090;
    unsigned int unk094;
    unsigned int unk098;
    unsigned int unk09c;
    unsigned int unk0a0;
    unsigned int unk0a4;
    unsigned int unk0a8;
    unsigned int unk0ac;
    unsigned int unk0b0;
    unsigned int unk0b4;
    unsigned int unk0b8;
    unsigned int unk0bc;
    unsigned int unk0c0;
    unsigned int unk0c4;
    unsigned int unk0c8;
    unsigned int unk0cc;
    unsigned int unk0d0;
    unsigned int unk0d4;
    unsigned int unk0d8;
    unsigned int unk0dc;
    unsigned int unk0e0;
    unsigned int unk0e4;
    unsigned int unk0e8;
    unsigned int unk0ec;
    unsigned int unk0f0;
    unsigned int unk0f4;
    unsigned int unk0f8;
    unsigned int unk0fc;
    unsigned int unk100;
    unsigned int unk104;
    unsigned int unk108;
    unsigned int unk10c;
    unsigned int unk110;
    unsigned int unk114;
    unsigned int unk118;
    unsigned int unk11c;
    unsigned int unk120;
    unsigned int unk124;
    unsigned int unk128;
    unsigned int unk12c;
    unsigned int unk130;
    unsigned int unk134;
    unsigned int unk138;
    unsigned int unk13c;
    unsigned int unk140;
    unsigned int unk144;
    unsigned int unk148;
    unsigned int unk14c;
    unsigned int unk150;
    unsigned int unk154;

    BSFile(const char*,int,unsigned int,bool);
    virtual ~BSFile();
    void FUN_00aff300(int,int);
    void FUN_00aff950(char*,unsigned int);
    void FUN_00affd10();
};
struct UserInterface {
    void** vtable;
    NiTexture* FUN_005f36f0();
    NiTexture* FUN_004fd3e0();
    const char* FUN_0045cd60();
    const char* FUN_0059bb30();
};
extern char DAT_0103b268;
extern char DAT_0103b258;
extern char DAT_0103b248;
extern char DAT_0103b238;
extern char DAT_0103b228;
extern char DAT_0103b1fc;
extern char DAT_0103b1d4;
extern char DAT_0103b1a8;
extern char DAT_01039664;
extern char DAT_0103964c;
extern char DAT_01039634;
extern char DAT_0103962c;
extern char DAT_01039624;
extern char DAT_01039618;
extern char DAT_01039608;
extern char DAT_010395f8;
extern char DAT_010395ec;
extern char DAT_010395e0;
extern char DAT_010395d0;
extern char DAT_010395c8;
extern char DAT_010395c0;
extern char DAT_010395b4;
extern char DAT_010395ac;
extern char DAT_010395a0;
extern char DAT_01039598;
extern char DAT_01039590;
extern char DAT_01039588;
extern char DAT_01039584;
extern char DAT_0103957c;
extern char DAT_01039578;
extern char DAT_01039570;
extern char DAT_01039568;
extern char DAT_01039564;
extern char DAT_01039560;
extern char DAT_0103952c;
extern char DAT_01023014;
extern char DAT_011f444c;
extern double DAT_0101ece0;
extern bool __cdecl FUN_005accb0(void*,void*,void*,void*,void*,void*,void*,char*);
extern int __cdecl FUN_00406d00(char*,...);
extern int __cdecl FUN_00406d30(char*,...);
extern int __cdecl FUN_004046f0(const char*,const char*);
extern int __cdecl FUN_0043b2b0(int);
extern unsigned int __cdecl FUN_005b5e40(void*,...);
extern void __cdecl FUN_00403d30(void*,int,unsigned int);
extern NiTexture* __cdecl FUN_00456510();
extern bool __cdecl FUN_0043b300(void*,NiTexture*);
extern char* __cdecl FUN_004afb00(char*,unsigned int);
extern int __cdecl FUN_004812f0(const char*, const char*);
extern unsigned int __cdecl FUN_00e7bd20(unsigned int);
extern unsigned int __cdecl FUN_00e7a9a0(unsigned int);
extern unsigned int __cdecl FUN_00ec6130(const char*);
unsigned char __cdecl FUN_005c5a70(void* source, void* callback, void* third, void* fourth,
                                     void* fifth, void* sixth, void* seventh, void* eighth) {
    char outPath[512];
    outPath[0]=0;
    if (source) {
        if (!FUN_005accb0(source,callback,eighth,third,fourth,fifth,sixth,outPath))
            return 0;
    }
    if (!outPath[0]) {
        NiTexture* active=((UserInterface*)DAT_011dea10)->FUN_005f36f0();
        if (active) {
            FUN_00406d00(outPath,512,&DAT_0103b258,&DAT_0103b268,active->v76());
        } else {
            NiTexture* queued=((UserInterface*)DAT_011dea10)->FUN_004fd3e0();
            if (queued) {
                FUN_00406d00(outPath,512,&DAT_0103b248,&DAT_0103b268,queued->v76(),
                             ((UserInterface*)DAT_011dea10)->FUN_0059bb30(),((UserInterface*)DAT_011dea10)->FUN_0045cd60());
            } else {
                FUN_00406d00(outPath,512,&DAT_0103b238,&DAT_0103b268);
            }
        }
    }
    if (!outPath[0])
        FUN_004046f0(outPath,&DAT_0103b228);
    FUN_0043b2b0(1);
    FUN_005b5e40((void*)&DAT_0103b1fc);
    BSFile output(outPath,1,0x4000,0);
    output.FUN_00aff300(0,0);
    const int iMax=2048;
    NiPointer<NiTexture> largest[2048];
    FUN_00403d30(largest,0,0x2000);
    unsigned int uiTotalSize=0;
    unsigned int numItems=0;
    NiTexture* pTex;
    pTex=FUN_00456510();
    while (pTex) {
        ++numItems;
        if (pTex->FUN_0059bb30()) {
            unsigned int size=FUN_005b5e40((void*)pTex);
            uiTotalSize+=size;
            int insertion=-1;
            for (int slot=0;slot<2048 && insertion==-1;++slot) {
                if (!largest[slot].operator NiTexture*()) {
                    insertion=slot;
                } else {
                    unsigned int existingSize=FUN_005b5e40((void*)largest[slot].operator NiTexture*());
                    if (existingSize<size) insertion=slot;
                }
            }
            if (insertion!=-1) {
                for (int slot=2047;slot>insertion;--slot)
                    largest[slot]=largest[slot-1];
                largest[insertion]=pTex;
            }
        }
        pTex=pTex->FUN_0055b980();
    }
    FUN_005b5e40((void*)&DAT_0103b1d4,numItems,(double)uiTotalSize/DAT_0101ece0);
    for (int i=0;i<2048;++i) {
        if (largest[i].operator NiTexture*()) {
            const char* category;
            char temp[260];
            char line[512];
            bool bUnnamed=false;
            if (FUN_0043b300(&DAT_011f444c,largest[i].operator NiTexture*())) {
                NiTexture* pkTexture=largest[i].operator NiTexture*();
                const char* label=pkTexture->v39()->operator const char*();
                if (!label || !label[0]) label=largest[i].operator NiTexture*()->FUN_00413f40()->operator const char*();
                if (!label || !label[0]) FUN_00406d30(temp,0x104,&DAT_01039664);
                else FUN_00406d30(temp,0x104,label);
            } else {
                bUnnamed=true;
                const char* label=largest[i].operator NiTexture*()->FUN_00413f40()->operator const char*();
                if (label && label[0]) FUN_00406d00(temp,0x104,&DAT_0103964c,label);
                else FUN_00406d00(temp,0x104,&DAT_01039634);
            }
            FUN_004afb00(temp,0x104);
            category=&DAT_0103962c;
            if (!bUnnamed) {
                if (FUN_004812f0(temp,&DAT_01039624) || FUN_004812f0(temp,&DAT_01039618) || FUN_004812f0(temp,&DAT_01039608) || FUN_004812f0(temp,&DAT_010395f8) || FUN_004812f0(temp,&DAT_010395ec) || FUN_004812f0(temp,&DAT_010395e0) || FUN_004812f0(temp,&DAT_010395d0)) category=&DAT_010395c8;
                else if (FUN_004812f0(temp,&DAT_010395c0) || FUN_004812f0(temp,&DAT_010395b4)) category=&DAT_010395ac;
                else if (FUN_004812f0(temp,&DAT_010395a0) || FUN_004812f0(temp,&DAT_01039598)) category=&DAT_01039590;
                else if (FUN_004812f0(temp,&DAT_01039588)) category=&DAT_01039584;
                else if (FUN_004812f0(temp,&DAT_0103957c)) category=&DAT_01039578;
                else if (FUN_004812f0(temp,&DAT_01039570)) category=&DAT_01023014;
                else category=&DAT_01039568;
            }
            unsigned int count=FUN_005b5e40((void*)largest[i].operator NiTexture*());
            unsigned int rawFormat=FUN_00e7bd20(largest[i].operator NiTexture*()->FUN_0059bb30()->FUN_007d6bb0());
            unsigned int uiBits=FUN_00e7a9a0(rawFormat);
            NiTexture* pkImage=largest[i].operator NiTexture*()->v2()->operator NiTexture*();
            FUN_00406d00(line,0x200,&DAT_0103952c,i+1,category,temp,
                         largest[i].operator NiTexture*()->v37(),
                         largest[i].operator NiTexture*()->v38(),
                         count>>10,uiBits,largest[i].operator NiTexture*()->FUN_00726070()-1,
                         largest[i].operator NiTexture*()->FUN_0043c430()==3?&DAT_01039564:&DAT_01039560,pkImage);
            FUN_005b5e40((void*)line);
            output.FUN_00aff950(line,FUN_00ec6130(line)+1);
        }
    }
    output.FUN_00affd10();
    FUN_005b5e40((void*)&DAT_0103b1a8);
    FUN_0043b2b0(0);
    return 1;
}
