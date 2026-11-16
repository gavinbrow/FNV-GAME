struct PointCalc : NiPoint3 {
    PointCalc FUN_00439ef0(const NiPoint3& other) const;
    double FUN_004a7290() const;
};
struct DistanceCheck {
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c, unk20, unk24;
    PointCalc firstPoint;
    PointCalc secondPoint;
    bool FUN_006e4840(const NiPoint3& point);
};
bool DistanceCheck::FUN_006e4840(const NiPoint3& point) {
    PointCalc vecA = firstPoint.FUN_00439ef0(point);
    PointCalc vecB = secondPoint.FUN_00439ef0(point);
    if (vecA.FUN_004a7290() < vecB.FUN_004a7290())
        return true;
    return false;
}
