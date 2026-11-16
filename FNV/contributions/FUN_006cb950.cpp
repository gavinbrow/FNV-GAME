// Detailed path construction between two solution nodes.
struct LenS {
    float FUN_00589850();
};
struct DoorHandle {
    const NavMeshInfo* mesh;
    unsigned short triangle;
    unsigned short flags;
    int edge;
    NiPoint3 position;
};
struct DoorAccess {
    DoorHandle* FUN_006cee10(int index);
};
struct LocAcc {
    bool FUN_0076b610();
    DoorHandle* FUN_006cedf0();
};
struct FUN_006cf180 {
    void** vt;
    void* buf;
    unsigned int sz;
    unsigned int res;
    FUN_006cf180();
    ~FUN_006cf180();
    unsigned int FUN_0044ddc0();
    void* FUN_00691750(int idx);
    int FUN_006cedd0(int a, int b);
    int FUN_006cedd0(int a);
};
struct FUN_006cf200 {
    void** vt;
    void* buf;
    unsigned int sz;
    unsigned int res;
    FUN_006cf200();
    ~FUN_006cf200();
};
struct NodeS {
    void* FUN_00717e50();
    bool FUN_006ca0c0();
    void* FUN_0055b980();
};
struct PosS {
    NiPoint3 FUN_005c3420();
};
struct MinS {
    unsigned int FUN_00441110();
};
struct SolS {
    void* FUN_006e78b0(unsigned int idx);
    void* FUN_006b05a0();
    bool FUN_006b05d0();
    void FUN_0069f920(void* elem, const NiPoint3& z);
};
struct PBX {
    int FUN_006caa40(unsigned int a, void* arr, void* loc);
    int FUN_006cac90(unsigned int a, void* arr, void* loc);
    bool FUN_006cb6a0(unsigned int a, void* arr, void* loc);
    int FUN_006cc5e0(int a);
};
struct ReqX {
    float FUN_0069ef80() const;
};
struct SettingCollX {
    float* Float();
};
extern SettingCollX DAT_011d6ef0;
struct _Mem_2064 {
    void** vtable;
    NiPoint3 position;
    const NavMeshInfo* mesh;
    const void* meshes;
    void* cell;
    void* world;
    unsigned int cellKey;
    unsigned short triangle;
    unsigned char flags;
    unsigned char padding;
    _Mem_2064(const NiPoint3& p, const void* nm, unsigned short tri);
    ~_Mem_2064();
};
struct PLArr {
    unsigned int FUN_006cf1b0(const PathingLocation& loc);
};
bool __cdecl FUN_006d7350(PathingLocation& a, PathingLocation& b, PathingLocation* c, void* d);


bool PathBuilder::FUN_006cb950(unsigned int a, unsigned int b)
{
    struct FUN_006cf200 distA; // Start door handles.
    struct FUN_006cf180 arrB; // Start path.
    // Start path result.
    int distB;
    int distC = ((PBX*)this)->FUN_006caa40(a, &arrB, &distA);
    struct FUN_006cf200 flag; // Goal door handles.
    struct FUN_006cf180 locA; // Goal path.
    // Goal path result.
    distB = ((PBX*)this)->FUN_006cac90(b, &locA, &flag);
    if (distC == 0 || distB == 0) {
        return false;
    }
    // Distance from the start to its door.
    float locB = 0.0f;
    if (!((LocAcc*)&distA)->FUN_0076b610()) {
        NiPoint3 ptA = ((DoorAccess*)&distA)->FUN_006cee10(0)->position;
        locB = ((LenS*)&(ptA - ((PosS*)((NodeS*)((SolS*)pSolution)->FUN_006e78b0(a))->FUN_00717e50())->FUN_005c3420()))->FUN_00589850();
    }
    // Distance from the goal to its door.
    float res2 = 0.0f;
    if (!((LocAcc*)&flag)->FUN_0076b610()) {
        NiPoint3 ptB = ((DoorAccess*)&flag)->FUN_006cee10(0)->position;
        res2 = ((LenS*)&(ptB - ((PosS*)((NodeS*)((SolS*)pSolution)->FUN_006e78b0(b))->FUN_00717e50())->FUN_005c3420()))->FUN_00589850();
    }
    // Direct endpoint distance.
    float r2 = ((LenS*)&(((PosS*)((NodeS*)((SolS*)pSolution)->FUN_006e78b0(a))->FUN_00717e50())->FUN_005c3420() - ((PosS*)((NodeS*)((SolS*)pSolution)->FUN_006e78b0(b))->FUN_00717e50())->FUN_005c3420()))->FUN_00589850();
    // Try a direct detailed path.
    bool r1 = false;
    if (2.0 * (locB + res2) > r2)
        r1 = true;
    if (distC == 2 || distB == 2) {
        if (r2 < 512.0)
            r1 = true;
    }
    if (r1) {
        struct FUN_006cf180 arrC;
        int res = ((PathBuilder_6cb4c0*)this)->FUN_006cb4c0(*(PathingLocation*)((NodeS*)((SolS*)pSolution)->FUN_006e78b0(a))->FUN_00717e50(), *(PathingLocation*)((NodeS*)((SolS*)pSolution)->FUN_006e78b0(b))->FUN_00717e50(), &arrC);
        switch (res) {
        case 1: {
            unsigned int nodeB; // Detailed-path index.
            for (nodeB = 0; nodeB < arrC.FUN_0044ddc0(); nodeB++)
                ((SolS*)pSolution)->FUN_0069f920(arrC.FUN_00691750(nodeB), NiPoint3::ZERO);
            // Goal solution node.
            void* i = ((SolS*)pSolution)->FUN_006e78b0(b);
            if (((NodeS*)i)->FUN_006ca0c0()) {
                ((Mid*)((SolS*)pSolution)->FUN_006b05a0())->FUN_006cc560((int)((NodeS*)i)->FUN_0055b980());
            } else if (((MinS*)((NodeS*)i)->FUN_00717e50())->FUN_00441110() != 0) {
                if ((unsigned int)pSolution->FUN_005a4320() > b + 1) {
                    if (((MinS*)((NodeS*)((SolS*)pSolution)->FUN_006e78b0(b + 1))->FUN_00717e50())->FUN_00441110()
                        == ((MinS*)((NodeS*)i)->FUN_00717e50())->FUN_00441110()) {
                        ((SolS*)pSolution)->FUN_0069f920(((NodeS*)((SolS*)pSolution)->FUN_006e78b0(b + 1))->FUN_00717e50(), NiPoint3::ZERO);
                        ((FUN_006cc5a0_shell*)((SolS*)pSolution)->FUN_006b05a0())->FUN_006cc5a0(true);
                    }
                }
            }
            return true;
            break;
        }
        case 0:
            return false;
        }
    }
    if (distC == 2) {
        return false;
    }
    if (distB == 2) {
        if (((LocAcc*)&flag)->FUN_0076b610()) {
            return false;
        }
        if (!((PBX*)this)->FUN_006cb6a0(b, &flag, &locA))
            pSolution->FUN_006c9fa0(1);
        {
            _Mem_2064 tmpPL(((LocAcc*)&flag)->FUN_006cedf0()->position,
                            ((LocAcc*)&flag)->FUN_006cedf0()->mesh,
                            ((LocAcc*)&flag)->FUN_006cedf0()->triangle);
            ((PLArr*)&locA)->FUN_006cf1b0(*(PathingLocation*)&tmpPL);
        }
    }
    {
        unsigned int i;
        for (i = 0; i < arrB.FUN_0044ddc0() - 1; i++)
            ((SolS*)pSolution)->FUN_0069f920(arrB.FUN_00691750(i), NiPoint3::ZERO);
    }
    // Combined path result.
    int arrA = ((PBX*)this)->FUN_006cc5e0(arrB.FUN_006cedd0(locA.FUN_006cedd0(a, b)));
    switch (arrA) {
    case 2: {
        if (r2 < 512.0 && (double)((ReqX*)pRequest)->FUN_0069ef80() < (double)*DAT_011d6ef0.Float()) {
        if (FUN_006d7350(*(PathingLocation*)((NodeS*)((SolS*)pSolution)->FUN_006e78b0(a))->FUN_00717e50(), *(PathingLocation*)((NodeS*)((SolS*)pSolution)->FUN_006e78b0(b))->FUN_00717e50(), 0, 0)) {
            return false;
        }
        struct FUN_006cf180 res3; // Retry path.
        // Retry path result.
        int arrD = ((PathBuilder_6cb4c0*)this)->FUN_006cb4c0(*(PathingLocation*)((NodeS*)((SolS*)pSolution)->FUN_006e78b0(a))->FUN_00717e50(), *(PathingLocation*)((NodeS*)((SolS*)pSolution)->FUN_006e78b0(b))->FUN_00717e50(), &res3);
        if (arrD != 1) {
            return false;
        }
        else {
        pSolution->FUN_006c9fa0(0);
        unsigned int i;
        for (i = 0; i < res3.FUN_0044ddc0(); i++)
            ((SolS*)pSolution)->FUN_0069f920(res3.FUN_00691750(i), NiPoint3::ZERO);
        return !((SolS*)pSolution)->FUN_006b05d0();
            }
        } else {
            return false;
        }
        break;
    }
    case 0: {
        if (!((LocAcc*)&locA)->FUN_0076b610()) {
            int i;
            for (i = (int)locA.FUN_0044ddc0() - 1; i >= 0; i--)
                ((SolS*)pSolution)->FUN_0069f920(locA.FUN_00691750(i), NiPoint3::ZERO);
        }
        void* nodeB = ((SolS*)pSolution)->FUN_006e78b0(b);
        if (((NodeS*)nodeB)->FUN_006ca0c0()) {
            ((Mid*)((SolS*)pSolution)->FUN_006b05a0())->FUN_006cc560((int)((NodeS*)nodeB)->FUN_0055b980());
        } else if (((MinS*)((NodeS*)nodeB)->FUN_00717e50())->FUN_00441110() != 0) {
            if ((unsigned int)pSolution->FUN_005a4320() > b + 1) {
                if (((MinS*)((NodeS*)((SolS*)pSolution)->FUN_006e78b0(b + 1))->FUN_00717e50())->FUN_00441110()
                    == ((MinS*)((NodeS*)nodeB)->FUN_00717e50())->FUN_00441110()) {
                    ((SolS*)pSolution)->FUN_0069f920(((NodeS*)((SolS*)pSolution)->FUN_006e78b0(b + 1))->FUN_00717e50(), NiPoint3::ZERO);
                    ((FUN_006cc5a0_shell*)((SolS*)pSolution)->FUN_006b05a0())->FUN_006cc5a0(true);
                }
            }
        }
        return !((SolS*)pSolution)->FUN_006b05d0();
        break;
    }
    case 1: {
        pSolution->FUN_006c9fa0(1);
        return false;
    }
    }
    return false;
}
