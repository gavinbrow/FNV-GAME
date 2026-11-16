
extern "C" void __cdecl FUN_0044f570();
extern "C" char DAT_010c28cc;
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
namespace fnv_0095c9c0 {
struct ResetSetting {
    FUN_0045cf30 member;
    ResetSetting(const char*,float);
    __forceinline ~ResetSetting() {}
};
ResetSetting DAT_01203168(&DAT_010c28cc,75.0f);
}
