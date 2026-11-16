
extern "C" void __cdecl FUN_0044f570();
extern "C" char DAT_010c2820;
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
class SettingT_GameSettingCollection_ {
 FUN_0045cf30 member;
public:
 SettingT_GameSettingCollection_(const char*,float);
 __forceinline ~SettingT_GameSettingCollection_() {}
};
SettingT_GameSettingCollection_ g_01203120(&DAT_010c2820,1700.0f);
