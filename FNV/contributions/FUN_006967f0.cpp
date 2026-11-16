struct TriList2 : public NavMeshTriList {
    void FUN_0069add0(int idx, int n);
};
bool __cdecl FUN_0069b2a0(const unsigned short& a, const unsigned short& b);
extern const float DAT_01016970;
struct Ov2 : public NavMeshOverlap {
    bool FUN_006967f0(unsigned short ausStart, unsigned short ausEnd);
};
bool Ov2::FUN_006967f0(unsigned short ausStart, unsigned short ausEnd)
{
    unsigned int i;
    for (i = ausStart; i <= ausEnd; i++) {
        NavMeshTriangle* pTri = GetTriangle((unsigned short)i);
        NiPoint3Ex fStack_14(DAT_01016970, DAT_01016970, 0.0f);
        NiPoint3Ex f(DAT_01015f5c, DAT_01015f5c, 0.0f);
        for (int j = 0; j < 3; j++) {
            const NiPoint3* pV = &FUN_0068f0a0(pTri->FUN_005582d0(j));
            if (pV->x < fStack_14.x) fStack_14.x = pV->x;
            if (pV->x > f.x) f.x = pV->x;
            if (pV->y < fStack_14.y) fStack_14.y = pV->y;
            if (pV->y > f.y) f.y = pV->y;
        }
        unsigned int j = 0, cf = 0, b = 0, p = 0;
        Grid.FUN_006912a0(fStack_14, j, cf);
        Grid.FUN_006912a0(f, b, p);
        for (unsigned int r = j; r <= b; r++) {
            for (unsigned int c = cf; c <= p; c++) {
                int idx;
                TriList2* pList = (TriList2*)Grid.FUN_006967c0(c, r);
                idx = pList->FUN_0069b240(*(unsigned short*)&i, 0, FUN_0069b2a0);
                pList->FUN_0069add0(idx, 1);
            }
        }
    }
    return true;
}


