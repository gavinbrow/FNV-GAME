struct FUN_0050eb90_Point3
{
    float x, y, z;
    void FUN_00416870(float x, float y, float z);
};
struct FUN_0050eb90_Component
{
    float FUN_0050eb30();
    float FUN_0050eb50();
    float FUN_0050eb70();
};
struct FUN_0050eb90_Class
{
    unsigned int unk00, unk04, unk08, unk0c, unk10, unk14;
    unsigned int unk18, unk1c, unk20, unk24;
    unsigned short unk28;
    FUN_0050eb90_Component component;
    FUN_0050eb90_Point3 FUN_0050eb90();
};
FUN_0050eb90_Point3 FUN_0050eb90_Class::FUN_0050eb90()
{
    FUN_0050eb90_Point3 result;
    result.FUN_00416870(component.FUN_0050eb30(),
                       component.FUN_0050eb50(),
                       component.FUN_0050eb70());
    return result;
}