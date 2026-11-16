// @fnv 0x00fdc1f0
struct ISetCollection { virtual void dummy0(); virtual void dummy1(); virtual void unregisterSetting(void*); };
extern ISetCollection* DAT_011f96a0;
extern "C" void FUN_0044f570();
struct __declspec(novtable) Setting {void FUN_00404950(); virtual __forceinline ~Setting(){ FUN_00404950(); }};
struct FUN_0045cf30: Setting {
  virtual void FUN_0045cf30_virtual();
  __forceinline ~FUN_0045cf30(){
    volatile unsigned int local0,local1,local2,local3;
    ISetCollection* collection;
    FUN_0044f570();
    collection=DAT_011f96a0;
    collection->unregisterSetting(this);
  }
};
class Setting_01017720_011f96a0 {public: FUN_0045cf30 data; __forceinline ~Setting_01017720_011f96a0(){}};
Setting_01017720_011f96a0 g_011f7160;