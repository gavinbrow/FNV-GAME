struct Setting_00ad9da0;
struct INIPrefSettingCollection { virtual void unknown0(); virtual void unknown1(); virtual void Remove(void*); };
extern "C" INIPrefSettingCollection* DAT_011f35a0;
extern "C" char DAT_01022738;
void FUN_004de4a0();
struct Setting { void* vftable; void FUN_00404950(); ~Setting() { FUN_00404950(); } };
struct SettingT_INI : Setting {
  ~SettingT_INI() {
    int spare1, spare2, spare3, spare4;
    FUN_004de4a0();
    INIPrefSettingCollection* c = DAT_011f35a0;
    c->Remove(this);
  }
};
struct Setting_00ad9da0 : SettingT_INI {
 ~Setting_00ad9da0() { vftable=&DAT_01022738; }
};
Setting_00ad9da0 g_011f6e38;