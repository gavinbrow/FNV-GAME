
extern "C" void __cdecl FUN_0044f570();
extern "C" char DAT_010c17dc;
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
class Setting_01017720_011f96a0 {
 FUN_0045cf30 member;
public:
 Setting_01017720_011f96a0(const char*,float);
 __forceinline ~Setting_01017720_011f96a0() {}
};
Setting_01017720_011f96a0 g_01202dc0(&DAT_010c17dc,50.0f);
