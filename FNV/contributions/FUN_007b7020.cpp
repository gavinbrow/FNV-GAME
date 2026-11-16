
struct RepairInventory {
    float FUN_004bcdb0(int mode);
    struct RepairForm* FUN_0044ddc0();
    int FUN_004be200(int mode, int active);
};
struct RepairForm {
    int FUN_00401170();
    float FUN_004be060();
    float FUN_004be180();
};
struct RepairTile {
    void FUN_00a012d0(int id, float value, int flag);
    void FUN_00700320(int id, int value);
    void FUN_00a01350(int id, const char* text);
    void FUN_00a01350(int id, const char* text, int flag);
    void FUN_00a01350(int id, int value);
};
struct RepairString {
    const char* FUN_00403df0(int);
};
struct RepairList {
    virtual void vf00();
    virtual int vf04();
    virtual void vf08();
    virtual void vf0c();
    virtual void vf10();
    virtual int vf14(int,int,int,int);
    virtual void vf18();
    virtual void vf1c();
    virtual void vf20(void (__cdecl *)());
    void FUN_007314c0(void (__cdecl *)(),int,int);
};
struct RepairMenuVirtual {
    virtual void vf00();
    virtual void vf04();
    virtual void vf08();
    virtual void vf0c();
    virtual void vf10(int,int);
};
struct RepairHud {
    int FUN_0066ef20(int);
};
struct RepairManager {
    void FUN_00715860();
    void FUN_00718630();
};
extern RepairInventory* DAT_011da760;
extern int DAT_011da74c;
extern RepairString DAT_011d2c7c;
extern RepairString DAT_011d396c;
extern RepairString DAT_011d20c4;
extern RepairHud* DAT_011dea3c;
extern const double DAT_01017a40;
extern const double DAT_01012060;
extern const char DAT_01047008[];
extern float __cdecl FUN_006450f0(RepairForm*,float,int,int);
extern float __cdecl FUN_004bd510(float,float);
extern float __cdecl FUN_00646360(int,float);
extern void __cdecl FUN_00406d30(char*,int,const char*);
extern void __cdecl FUN_007b57f0();
extern void __cdecl FUN_007b5950();
extern void __cdecl FUN_007b6aa0();
extern bool __cdecl FUN_004b71d0();
extern void __cdecl FUN_007044c0(int,int,int);
extern InterfaceManager* __stdcall FUN_004b7210(int);
extern InterfaceManager* __stdcall FUN_004b7210(int,int);
extern int __stdcall FUN_007b5720(int);

void __cdecl FUN_007b7020(int target)
{
    if (DAT_011da75c != 0) {
        if (target != 0) {
            DAT_011da760 = reinterpret_cast<RepairInventory*>(target);
        }
        float percent = DAT_011da760->FUN_004bcdb0(1) / DAT_01017a40;
        reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[4])->FUN_00a012d0(0x1004,percent,1);
        reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[4])->FUN_00700320(0xfa3,1);
        RepairForm* form = DAT_011da760->FUN_0044ddc0();
        int type = form->FUN_00401170();
        if (type == 0x28) {
            reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[5])->FUN_00a01350(DAT_011da74c,DAT_011d2c7c.FUN_00403df0(1));
            reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[5])->FUN_00700320(DAT_011da754,(int)FUN_004bd510(FUN_006450f0(form,percent,target,0),1.0f));
        } else if (type == 0x18) {
            RepairForm* branchForm = form;
            float low = FUN_00646360((int)branchForm->FUN_004be060(),percent);
            float maximum = FUN_00646360((int)branchForm->FUN_004be180(),percent);
            if (maximum > DAT_01012060) {
                reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[5])->FUN_00a01350(DAT_011da74c,DAT_011d396c.FUN_00403df0(1));
                reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[5])->FUN_00700320(DAT_011da754,(int)maximum);
            } else if (low > DAT_01012060) {
                reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[5])->FUN_00a01350(DAT_011da74c,DAT_011d20c4.FUN_00403df0(1));
                reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[5])->FUN_00700320(DAT_011da754,(int)low);
            } else {
                char unavailableText[128];
                FUN_00406d30(unavailableText,128,DAT_01047008);
                reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[5])->FUN_00a01350(DAT_011da74c,DAT_011d20c4.FUN_00403df0(1));
                reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[5])->FUN_00a01350(DAT_011da754,unavailableText,1);
            }
        } else {
            char unavailableText[128];
            FUN_00406d30(unavailableText,128,DAT_01047008);
            reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[5])->FUN_00a01350(DAT_011da74c,DAT_011d20c4.FUN_00403df0(1));
            reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[5])->FUN_00a01350(DAT_011da754,unavailableText,1);
        }

        if (target != 0) {
            reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[3])->FUN_00a01350(0xfcc,DAT_011da760->FUN_004be200(0,1));
            FUN_007b6aa0();
        }
        reinterpret_cast<RepairList*>(&DAT_011da75c->lbRepairList)->FUN_007314c0(&FUN_007b57f0,0,0x7fffffff);
        reinterpret_cast<RepairList*>(&DAT_011da75c->lbRepairList)->vf20(&FUN_007b5950);
        reinterpret_cast<RepairTile*>(DAT_011da75c->pTiles[0])->FUN_00700320(DAT_011da754,reinterpret_cast<RepairHud*>(reinterpret_cast<char*>(DAT_011dea3c)+0xa4)->FUN_0066ef20(0x27));
        if (target && FUN_004b71d0()) {
            reinterpret_cast<RepairManager*>(FUN_004b7210(reinterpret_cast<RepairList*>(&DAT_011da75c->lbRepairList)->vf14(1,0,0xfc3,1)))->FUN_00715860();
        }
        reinterpret_cast<RepairMenuVirtual*>(DAT_011da75c)->vf10(0xe,reinterpret_cast<RepairList*>(&DAT_011da75c->lbRepairList)->vf04());
        if (target != 0) {
            FUN_007044c0(1,0,0);
            reinterpret_cast<RepairManager*>(reinterpret_cast<char*>(FUN_004b7210(6,FUN_007b5720(500)))+0x4d4)->FUN_00718630();
        }
    }
}