typedef PathSmootherPOVSearch::PathEdgeVert PathEdgeVertType;
typedef BSSimpleArray<PathEdgeVertType, 1024> EdgeVertArray;
struct NavMeshVertexAccess : NavMesh {
    const NiPoint3* FUN_0068f0a0(unsigned short);
};
struct FUN_006aeba0_shell : PathSmootherPOVSearch {
    void FUN_006aeba0(EdgeVertArray* vertices, unsigned int index, bool left);
};
extern const double DAT_01012060;
extern const double DAT_0103c7c8;
extern const double DAT_0106b9d8;
extern const double DAT_010290f0;

void FUN_006aeba0_shell::FUN_006aeba0(EdgeVertArray* vertices, unsigned int index, bool left)
{
    NiPoint3 point = *reinterpret_cast<NavMeshVertexAccess*>(
        reinterpret_cast<PathEdgeVertType*>(
          reinterpret_cast<FUN_006b3120_shell*>(vertices)->FUN_006b3120(index)
        )->pNavMesh
    )->FUN_0068f0a0(
        reinterpret_cast<PathEdgeVertType*>(
          reinterpret_cast<FUN_006b3120_shell*>(vertices)->FUN_006b3120(index)
        )->usVertex
    );
    NiPoint3 prevDir;
    NiPoint3 right;
    if (index == 0) {
        prevDir = StartLocation - point;
    } else {
        prevDir = *reinterpret_cast<NavMeshVertexAccess*>(
            reinterpret_cast<PathEdgeVertType*>(
                reinterpret_cast<FUN_006b3120_shell*>(vertices)->FUN_006b3120(index - 1)
            )->pNavMesh
        )->FUN_0068f0a0(
            reinterpret_cast<PathEdgeVertType*>(
                reinterpret_cast<FUN_006b3120_shell*>(vertices)->FUN_006b3120(index - 1)
            )->usVertex
        ) - point;
    }
    if (index == vertices->GetSize() - 1) {
        right = GoalLocation - point;
    } else {
        right = *reinterpret_cast<NavMeshVertexAccess*>(
            reinterpret_cast<PathEdgeVertType*>(
                reinterpret_cast<FUN_006b3120_shell*>(vertices)->FUN_006b3120(index + 1)
            )->pNavMesh
        )->FUN_0068f0a0(
            reinterpret_cast<PathEdgeVertType*>(
                reinterpret_cast<FUN_006b3120_shell*>(vertices)->FUN_006b3120(index + 1)
            )->usVertex
        ) - point;
    }
    prevDir.z = 0.0f;
    right.z = 0.0f;
    prevDir.UnitizeVector();
    right.UnitizeVector();
    NiPoint3 cross = left ? prevDir.UnitCross(right) : right.UnitCross(prevDir);
    float dot = right.Dot(prevDir);
    bool usePOV = false;
    if (index == 0 || index == vertices->GetSize() - 1) {
        usePOV = true;
    } else if (dot > DAT_01012060) {
        if (cross.z < DAT_0103c7c8) {
            usePOV = true;
        }
    } else if (cross.z < DAT_0106b9d8) {
        usePOV = true;
    }
    if (usePOV) {
        PathSmootherPOV* pov = new PathSmootherPOV;
        pov->eType = !left;
        pov->EdgeHandle = reinterpret_cast<PathEdgeVertType*>(
            reinterpret_cast<FUN_006b3120_shell*>(vertices)->FUN_006b3120(index)
        )->Edge;
        pov->Edge1 = prevDir;
        pov->Edge2 = right;
        pov->Center = point;
        pov->fCostFactor = 1.0f;
        pov->fRadius = pRequest->FUN_0069ef80() * DAT_010290f0;
        pov->iVertexIndex = reinterpret_cast<PathEdgeVertType*>(
            reinterpret_cast<FUN_006b3120_shell*>(vertices)->FUN_006b3120(index)
        )->usVertex;
        pov->iOtherSideIndex = -1;
        if (left) {
            pov->iThisSideIndex = LeftPOVs.GetSize();
        } else {
            pov->iThisSideIndex = RightPOVs.GetSize();
        }
        reinterpret_cast<PathEdgeVertType*>(
            reinterpret_cast<FUN_006b3120_shell*>(vertices)->FUN_006b3120(index)
        )->iPOVIndex = pov->iThisSideIndex;
        allPOVs.Add(pov);
        if (left) {
            LeftPOVs.Add(pov);
        } else {
            RightPOVs.Add(pov);
        }
    }
}