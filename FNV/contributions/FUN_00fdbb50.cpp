
extern "C" void __cdecl FUN_0044f570();
extern "C" char DAT_010a3850;
struct __declspec(novtable) Setting {virtual void first(); void FUN_00404950(); ~Setting(){FUN_00404950();}};
struct INISettingCollection{virtual void foo();virtual void bar();virtual void Remove(Setting*);};
extern "C" INISettingCollection* DAT_011f96a0;
struct FUN_0045cf30 : Setting {
virtual void first();
FUN_0045cf30(const char*,float);
__forceinline ~FUN_0045cf30(){
    volatile int pad[4];
    FUN_0044f570();
    INISettingCollection* c=DAT_011f96a0;
    c->Remove(this);
}
};
struct Setting_00ad9da0{
 FUN_0045cf30 member;
 Setting_00ad9da0(const char*,float);
 __forceinline ~Setting_00ad9da0() {}
};
namespace fnv_00adf080{
Setting_00ad9da0 g_011f6e80(&DAT_010a3850,6.0f);
}
