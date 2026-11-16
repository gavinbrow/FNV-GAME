extern const char* DAT_01268288;

struct FUN_00ca0ac0_class : SphereShape {
    void FUN_00ca0ac0(ViewerStringArray* strings);
};

void FUN_00ca0ac0_class::FUN_00ca0ac0(ViewerStringArray* strings)
{
    TlsGuard_t context;
    FUN_00c9fc50(strings);
    char* text = FUN_00a7d330(DAT_01268288);
    strings->Add(text);
}
