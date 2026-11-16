extern "C" void FUN_0044f570();
class Setting;
class INISettingCollection {public: virtual void m0(); virtual void m1(); virtual void Remove(Setting *);};
extern "C" INISettingCollection *DAT_011f96a0;
class __declspec(novtable) Setting {
public:
 virtual void vmethod();
 void FUN_00404950();
 __forceinline ~Setting(){FUN_00404950();}
};
class FUN_0045cf30 : public Setting {
public:
 virtual void vmethod();
 __forceinline ~FUN_0045cf30() {
  struct Local{INISettingCollection* p; int unused[4];}; Local local;
  FUN_0044f570(); local.p = DAT_011f96a0; local.p->Remove(this);
 }
};
class Setting_01017720_011f96a0 : public FUN_0045cf30 {};
Setting_01017720_011f96a0 g_011f3450;