class FNV_VirtualDevice {
public:
    virtual void vfn_00();
    virtual void vfn_01();
    virtual void vfn_02();
    virtual void vfn_03();
    virtual void vfn_04();
    virtual void vfn_05();
    virtual void vfn_06();
    virtual void vfn_07();
    virtual void vfn_08();
    virtual void vfn_09();
    virtual void vfn_0a();
    virtual void vfn_0b();
    virtual void vfn_0c();
    virtual void vfn_0d();
    virtual void vfn_0e();
    virtual void vfn_0f();
    virtual void vfn_10();
    virtual void vfn_11();
    virtual void vfn_12();
    virtual void vfn_13();
    virtual void vfn_14();
    virtual void vfn_15();
    virtual void vfn_16();
    virtual void vfn_17();
    virtual void vfn_18();
    virtual void vfn_19();
    virtual void vfn_1a(int code, int zero1, int zero2, int zero3);
    virtual void vfn_1b();
    virtual void vfn_1c();
    virtual void vfn_1d();
    virtual void vfn_1e();
    virtual void vfn_1f();
    virtual void vfn_20();
    virtual void vfn_21();
    virtual void vfn_22();
    virtual void vfn_23();
    virtual void vfn_24();
    virtual void vfn_25();
    virtual void vfn_26();
    virtual void vfn_27();
    virtual unsigned char vfn_28();
    virtual void vfn_29();
    virtual void vfn_2a();
    virtual void vfn_2b();
    virtual void vfn_2c();
    virtual void vfn_2d();
    virtual void vfn_2e();
    virtual void vfn_2f();
    virtual void vfn_30();
    virtual void vfn_31();
    virtual void vfn_32();
    virtual void vfn_33(int id, int oneOrTwo, int three, int zero);
};

extern FNV_VirtualDevice* DAT_0126f6c4;
extern FNV_VirtualDevice* DAT_0126f6c8;

class FUN_00e7dc90_Class {
public:
    unsigned int unknown00;
    int objectId;
    void __thiscall FUN_00e7dc90(bool enabled);
};

void __thiscall FUN_00e7dc90_Class::FUN_00e7dc90(bool enabled)
{
    if (!enabled)
        return;

    if (DAT_0126f6c4->vfn_28() & 8)
        return;
    if (!(DAT_0126f6c4->vfn_28() & 4))
        return;

    DAT_0126f6c8->vfn_33(objectId, 1, 3, 0);
    DAT_0126f6c8->vfn_33(objectId, 2, 3, 0);

    unsigned int code = 0xc6;
    for (unsigned int remaining = 8; remaining; --remaining) {
        DAT_0126f6c8->vfn_1a(code - 0x46, 0, 0, 0);
        DAT_0126f6c8->vfn_1a(code, 0, 0, 0);
        ++code;
    }
}