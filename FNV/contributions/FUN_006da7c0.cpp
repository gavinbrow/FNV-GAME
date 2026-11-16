struct CellOps { bool FUN_00425fd0(); int FUN_00544c30(); int FUN_00544c60(); };
struct LocationBench {
    void* table; NiPoint3 point; const NavMeshInfo* fMinX; const void* meshes;
    TESObjectCELL* cell; TESWorldSpace* world; unsigned int key; unsigned short triangle; unsigned char flags, padding;
    LocationBench(const NiPoint3&, CellOps*); LocationBench(const NiPoint3&, void*); ~LocationBench();
    bool FUN_006dd6f0(int); void FUN_006dd610(NavMeshPtr&); void* FUN_00441110();
};
struct PointArrayBench {
    void* table; NiPoint3* data; unsigned int size, capacity;
    PointArrayBench(unsigned int); ~PointArrayBench(); NiPoint3& FUN_006a1440(unsigned int);
};
struct Point2Bench { float x,y; Point2Bench(); Point2Bench(float,float); };
struct CloseRequestBench {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6c;
    unsigned int unk70;
    unsigned int unk74;
    unsigned int unk78;
    unsigned int unk7c;
    unsigned int unk80;
    unsigned int unk84;
    unsigned int unk88;
    unsigned int unk8c;
    unsigned int unk90;
    unsigned int unk94;
    unsigned int unk98;
    unsigned int unk9c;
    unsigned int unka0;
    unsigned int unka4;
    unsigned int unka8;
    unsigned int unkac;
    unsigned int unkb0;
    unsigned int unkb4;
    unsigned int unkb8;
    unsigned int unkbc;
    unsigned int unkc0;
    unsigned int unkc4;
    unsigned int unkc8;
    unsigned int unkcc;
    unsigned int unkd0;
    unsigned int unkd4;
    unsigned int unkd8;
    unsigned int unkdc;
    unsigned int unke0;
    unsigned int unke4;
    unsigned int unke8;
    unsigned int unkec;
    CloseRequestBench(); ~CloseRequestBench();
    void FUN_006d3ac0(const LocationBench&); void FUN_006dad40(const NiPoint3&); void FUN_006d1bc0(const LocationBench&);
};
struct CloseSolutionBench {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    CloseSolutionBench(); ~CloseSolutionBench();
};
struct RequestBench {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4c;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5c;
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6c;
    unsigned int unk70;
    unsigned int unk74;
    unsigned int unk78;
    unsigned int unk7c;
    unsigned int unk80;
    unsigned int unk84;
    unsigned int unk88;
    unsigned int unk8c;
    unsigned int unk90;
    unsigned int unk94;
    unsigned int unk98;
    unsigned int unk9c;
    unsigned int unka0;
    unsigned int unka4;
    unsigned int unka8;
    unsigned int unkac;
    RequestBench(); ~RequestBench();
    void FUN_006d3ac0(const LocationBench&); void FUN_006dad40(const NiPoint3&); void FUN_006d1bc0(const LocationBench&);
};
struct SolutionBench {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3c;
    unsigned int unk40;
    unsigned int unk44;
    SolutionBench(); ~SolutionBench();
};
extern const NiPoint3 DAT_011f426c;
float __cdecl RandomFloat(float,float);
bool __cdecl FUN_006d7110(void*,int,const NiPoint3&,float,NiPoint3&);
bool __cdecl FUN_006b9e90(const Point2Bench&,const Point2Bench&,const Point2Bench&,const Point2Bench&,Point2Bench&);
extern "C" bool __cdecl FUN_006ba010(const Point2Bench&,const Point2Bench&,const Point2Bench&,const Point2Bench&);
void __cdecl FNV_Warning(const char*);
bool __cdecl FUN_006d62e0(CloseRequestBench*,CloseSolutionBench*);
bool __cdecl BuildBench(RequestBench*,SolutionBench*);
float __cdecl FUN_006da7c0(CellOps* cell,const NiPoint3& pos,int mode,unsigned int count) {
    float eType;
    int kPosition;
    NiPoint3 bInterior;
    NavMeshPtr fMinX;
    bInterior = DAT_011f426c;
    float kRange = 500.0f;
    kPosition = mode;
    bool fMaxY = cell->FUN_00425fd0();
    float kPoints, kNavMesh, kLocation;
    if (fMaxY) { kPoints=-kRange; eType=-kRange; kNavMesh=kRange; kLocation=kRange; }
    else { kPoints=float(cell->FUN_00544c30()<<12); eType=float(cell->FUN_00544c60()<<12); kNavMesh=kPoints+4096.0; kLocation=eType+4096.0; }
    LocationBench fMinY(pos,cell);
    if (!fMinY.FUN_006dd6f0(0)) return 0.0f;
    fMinY.FUN_006dd610(fMinX);
    PointArrayBench fMaxX(count);
    if (kPosition == 2) {
        for (unsigned int i=0;i<count;i++) {
            if (!FUN_006d7110(fMinY.FUN_00441110(),0,pos,2000.0f,fMaxX.FUN_006a1440(i))) i--;
        }
    } else {
        for (unsigned int j=0;j<count;j++) {
            fMaxX.FUN_006a1440(j).x=RandomFloat(kPoints,kNavMesh);
            fMaxX.FUN_006a1440(j).y=RandomFloat(eType,kLocation);
            fMaxX.FUN_006a1440(j).z=pos.z;
        }
    }
    for (unsigned int k=0;k<count;k++) {
        switch(kPosition) {
        case 0: {
            bool kPoint3;
            Point2Bench bFirst;
            Point2Bench kPoint1(fMaxX.FUN_006a1440(k).x,fMaxX.FUN_006a1440(k).y);
            Point2Bench bSecond(fMaxX.FUN_006a1440((k+1)%count).x,fMaxX.FUN_006a1440((k+1)%count).y);
            Point2Bench kPoint2(fMaxX.FUN_006a1440((k+2)%count).x,fMaxX.FUN_006a1440((k+2)%count).y);
            Point2Bench kPoint0(fMaxX.FUN_006a1440((k+3)%count).x,fMaxX.FUN_006a1440((k+3)%count).y);
            kPoint3=FUN_006b9e90(kPoint1,bSecond,kPoint2,kPoint0,bFirst);
            bool testResult=FUN_006ba010(kPoint1,bSecond,kPoint2,kPoint0);
            if (kPoint3!=testResult) FNV_Warning("PATHFINDING: Different");
            break;
        }
        case 1: {
            CloseRequestBench request;
            request.FUN_006d3ac0(fMinY);
            request.FUN_006dad40(fMaxX.FUN_006a1440(k));
            CloseSolutionBench solution;
            FUN_006d62e0(&request,&solution);
            break;
        }
        case 2: {
            LocationBench goal(fMaxX.FUN_006a1440(k),fMinY.FUN_00441110());
            RequestBench request;
            request.FUN_006d3ac0(fMinY);
            request.FUN_006d1bc0(goal);
            SolutionBench solution;
            BuildBench(&request,&solution);
            break;
        }
        }
    }
    return 0.0f;
}
