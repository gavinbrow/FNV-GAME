struct RegionList {
    virtual ~RegionList();
};

struct ExtraRegionList : BSExtraData {
    RegionList* regions;
    ExtraRegionList(RegionList* value);
};

struct FUN_0041bbd0_shell : ExtraDataList {
    void FUN_0041bbd0(RegionList* value);
};

void FUN_0041bbd0_shell::FUN_0041bbd0(RegionList* value) {
    ExtraRegionList* data = static_cast<ExtraRegionList*>(GetExtraData(4));
    if (value == 0) {
        if (data)
            reinterpret_cast<Dummy_00410020*>(this)->FUN_00410020(data, true);
    } else if (data == 0) {
        data = new ExtraRegionList(value);
        AddExtra(data);
    } else {
        if (data->regions && data->regions != value)
            delete data->regions;
        data->regions = value;
    }
}
