extern unsigned char DAT_01017720;
extern "C" void __cdecl FUN_0044f570();
class INISettingCollection { public: virtual void entry0()=0; virtual void entry1()=0; virtual void unregisterSetting(void *)=0; };
extern INISettingCollection * DAT_011f96a0;
class Setting { public: void *vptr; void FUN_00404950(); ~Setting(){ FUN_00404950(); } };
class SettingT : public Setting { public: ~SettingT() {
  FUN_0044f570();
  INISettingCollection * collection = DAT_011f96a0;
  unsigned int spare0;
  unsigned int spare1;
  unsigned int spare2;
  unsigned int spare3;
  collection->unregisterSetting(this);
}};
class Setting_01017720_011f96a0 : public SettingT { public: ~Setting_01017720_011f96a0(){ vptr = &DAT_01017720; } };
Setting_01017720_011f96a0 g_01203174;
