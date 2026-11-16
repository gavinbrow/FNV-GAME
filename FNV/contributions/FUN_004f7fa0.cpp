extern float DAT_01016970;
extern const double DAT_010231b0;

struct RegionPointNode : BSSimpleList<TESRegionPoint*> {
    RegionPointNode* FUN_00726070();
};

struct FUN_004f7fa0_shell : TESRegionPointList {
    float FUN_004f7fa0();
};

float FUN_004f7fa0_shell::FUN_004f7fa0() {
    float minimumY = DAT_01016970;
    RegionPointNode* current = (RegionPointNode*)this;

    if (Minimums.y < DAT_010231b0) {
        return Minimums.y;
    }

    while (current && _ref_006815c0(current)) {
        if (_ref_006815c0(current)->GetY() < minimumY) {
            minimumY = _ref_006815c0(current)->GetY();
        }
        current = current->FUN_00726070();
    }
    return minimumY;
}