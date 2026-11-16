
struct TESRegionPointList_ref : TESRegionPointList {
    TESRegionPointList_ref(bool owns);
    bool FUN_004f7ca0(TESRegionPoint* point, float scale);
    TESRegionPointList_ref* FUN_00726070();
};
struct TESRegionPoint_ref : TESRegionPoint {
    TESRegionPoint* FUN_004f7130(int option);
};
struct FUN_004f80c0_shell : TESRegionPointList {
    TESRegionPointList* FUN_004f80c0(TESRegionPointList* out);
};
TESRegionPointList* FUN_004f80c0_shell::FUN_004f80c0(TESRegionPointList* out) {
    FUN_004f80c0_shell* current = this;
    TESRegionPointList* result = out ? out : new TESRegionPointList_ref(bOwnsPointMemory);
    TESRegionPoint* clonedPoint = 0;
    while (current != 0) {
        if (result->bOwnsPointMemory) {
            clonedPoint = reinterpret_cast<TESRegionPoint_ref*>(_ref_006815c0(current))->FUN_004f7130(0);
            if (!reinterpret_cast<TESRegionPointList_ref*>(result)->FUN_004f7ca0(clonedPoint, 0.0f)) {
                delete clonedPoint;
            }
        } else {
            reinterpret_cast<TESRegionPointList_ref*>(result)->FUN_004f7ca0(_ref_006815c0(current), 0.0f);
        }
        current = reinterpret_cast<FUN_004f80c0_shell*>(reinterpret_cast<TESRegionPointList_ref*>(current)->FUN_00726070());
    }
    return result;
}
