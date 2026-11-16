extern "C" int __cdecl FUN_00ec43fb(int, int, int*, int*, int);
extern int DAT_0119bdec;
extern int DAT_0119be3c;

struct FUN_0067f030 {
    int unk00;
    int unk04;
    int unk08;
    FUN_0067f030();
    ~FUN_0067f030();
    void __thiscall FUN_0067f4d0(void* location, int flags);
};

struct FUN_0067ba40_Result {
    int unk00;
    void* location;
};

struct TESEatPackageData_Copy {
    int unk00;
    FUN_0067f030* pSearchLocation;
    void __thiscall FUN_0067ba40(int flags);
};

void __thiscall TESEatPackageData_Copy::FUN_0067ba40(int flags) {
    FUN_0067ba40_Result* result = (FUN_0067ba40_Result*)FUN_00ec43fb(
        flags, 0, &DAT_0119bdec, &DAT_0119be3c, 0);
    if (result) {
        if (pSearchLocation) {
            delete pSearchLocation;
            pSearchLocation = 0;
        }
        if (result->location) {
            pSearchLocation = new FUN_0067f030;
            pSearchLocation->FUN_0067f4d0(result->location, 0);
        }
    }
}