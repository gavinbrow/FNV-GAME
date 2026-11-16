struct __declspec(align(16)) Quaternion {
    float x, y, z, w;
};
struct PackedTransform {
    Quaternion rotationColumn0;
    Quaternion rotationColumn1;
    Quaternion rotationColumn2;
    Quaternion translation;
    void FUN_00cb2240(int a, Quaternion* base);
};
struct Dispatch {
    virtual void vfn00();
    virtual void vfn04();
    virtual void vfn08();
    virtual void vfn0c();
    virtual void vfn10();
    virtual void vfn14();
    virtual void vfn18();
    virtual void vfn1c(PackedTransform* tmp, float factor, int flags);
};
struct FUN_00cf59e0_Class {
    int unk00; int unk04; int unk08; int unk0c; int unk10;
    Dispatch* dispatch;
    int unk18; int unk1c; int unk20; int unk24;
    int unk28; int unk2c;
    Quaternion quaternion;
    void FUN_00cf59e0(int a, float factor, int flags);
};
void FUN_00cf59e0_Class::FUN_00cf59e0(int a, float factor, int flags)
{
    PackedTransform transformed;
    transformed.FUN_00cb2240(a, &quaternion);
    dispatch->vfn1c(&transformed, factor, flags);
}