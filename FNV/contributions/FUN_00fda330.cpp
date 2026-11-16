extern "C" void FUN_0044f570();struct INISettingCollection{virtual void method0();virtual void method1();virtual void RemoveSetting(void *);};extern INISettingCollection* DAT_011f96a0;
class __declspec(novtable) Setting{public:virtual void getType()=0;void FUN_00404950();__forceinline ~Setting(){FUN_00404950();}};
class Setting_01017720_011f96a0:public Setting{public:virtual void getType();Setting_01017720_011f96a0(){}__forceinline ~Setting_01017720_011f96a0(){FUN_0044f570();int unused0,unused1,unused2,unused3;{INISettingCollection* collection=DAT_011f96a0;collection->RemoveSetting(this);}}};
Setting_01017720_011f96a0 g_011f33c8;
// @fnv 0x00fda330