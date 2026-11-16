// @fnv 0x00fde3d0
void FUN_0044f570();
struct FUN_0045cf30;
struct Collection {
    virtual void f0();
    virtual void f1();
    virtual void Remove(FUN_0045cf30*);
};
extern Collection* DAT_011f96a0;
class __declspec(novtable) Setting {
public:
    virtual void VirtualSetting() = 0;
    void FUN_00404950();
    __forceinline ~Setting() { FUN_00404950(); }
};
struct FUN_0045cf30 : Setting {
    virtual void VirtualSetting();
    __forceinline ~FUN_0045cf30() {
        int local0, local1, local2, local3;
        FUN_0044f570();
        Collection* c = DAT_011f96a0;
        c->Remove(this);
    }
};
class Setting_01017720_011f96a0 {
public:
    FUN_0045cf30 inner;
    __forceinline ~Setting_01017720_011f96a0() {}
};
Setting_01017720_011f96a0 g_0126fac8;