extern "C" void FUN_0044f570();
struct __declspec(novtable) Setting { virtual void placeholder()=0; void FUN_00404950(); __forceinline ~Setting(){FUN_00404950();} };
struct INISettingCollection {virtual void f0();virtual void f1();virtual void Remove(Setting*);};
extern "C" INISettingCollection* DAT_011f96a0;
union Cache { INISettingCollection *c; void *padding[5]; };
struct FUN_0045cf30 : Setting {
  virtual void placeholder();
  __forceinline ~FUN_0045cf30(){ FUN_0044f570(); Cache x; x.c=DAT_011f96a0; x.c->Remove(this); }
};
struct Setting_00ad9da0: FUN_0045cf30 {};
namespace fnv_00adf080 { Setting_00ad9da0 g_011f6e98; }