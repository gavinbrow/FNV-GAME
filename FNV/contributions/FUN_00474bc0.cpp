struct AmmoRecord {
    int __thiscall FUN_00401170();
};
struct ComparisonInfo {
    int __thiscall FUN_00484e60(int);
    int __thiscall FUN_00474cb0();
    unsigned int __thiscall FUN_0084e3a0();
};
void __cdecl FUN_00485d50(void**, int);
void* __cdecl FUN_004839c0(void*);
void __cdecl FUN_005b5e40(const char*, ...);
extern const char str_0101a3c8[];
extern const char str_0101a404[];
extern const char str_0101a444[];

struct FUN_00474bc0_shell : BaseFormComponent {
    void* pFormAmmo;
    void __thiscall FUN_00474bc0(BaseFormComponent*);
};
void __thiscall FUN_00474bc0_shell::FUN_00474bc0(BaseFormComponent* apCompareFC) {
    if (pFormAmmo) {
        void* oldAmmo = pFormAmmo;
        FUN_00485d50(&oldAmmo, reinterpret_cast<ComparisonInfo*>(apCompareFC)->FUN_00484e60(-1));
        pFormAmmo = FUN_004839c0(oldAmmo);
        if (pFormAmmo && reinterpret_cast<AmmoRecord*>(pFormAmmo)->FUN_00401170() != 0x29
            && reinterpret_cast<AmmoRecord*>(pFormAmmo)->FUN_00401170() != 0x55) {
            pFormAmmo = 0;
        }
        if (!pFormAmmo) {
            if (apCompareFC) {
                if (reinterpret_cast<ComparisonInfo*>(apCompareFC)->FUN_00474cb0()) {
                    FUN_005b5e40(str_0101a444, oldAmmo,
                        (reinterpret_cast<int (__thiscall *)(BaseFormComponent*)>((*reinterpret_cast<void***>(apCompareFC))[0x130 / 4]))(apCompareFC));
                } else {
                    FUN_005b5e40(str_0101a404, oldAmmo,
                        reinterpret_cast<DeallocHolder*>(apCompareFC)->_ref_0084e3a0());
                }
            } else {
                FUN_005b5e40(str_0101a3c8, oldAmmo);
            }
        }
    }
}