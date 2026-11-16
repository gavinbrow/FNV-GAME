extern "C" void FUN_004de4a0();
struct INIPrefSettingCollection {
    virtual void method0();
    virtual void method1();
    virtual void RemoveSetting(void *);
};
extern INIPrefSettingCollection *DAT_011f35a0;
class __declspec(novtable) Setting {
public:
    virtual void getType() = 0;
    void FUN_00404950();
    __forceinline ~Setting() { FUN_00404950(); }
};
class Setting_01022738_011f35a0 : public Setting {
public:
    virtual void getType();
    Setting_01022738_011f35a0() {}
    __forceinline ~Setting_01022738_011f35a0() {
        FUN_004de4a0();
        int unused0, unused1, unused2, unused3;
        {
            INIPrefSettingCollection *collection = DAT_011f35a0;
            collection->RemoveSetting(this);
        }
    }
};
Setting_01022738_011f35a0 g_011f6e44;
// @fnv 0x00fdb8d0
