class Setting_01017720_011f96a0;
struct Collection { virtual void unknown0(); virtual void unknown1(); virtual void Remove(void*); };
extern "C" Collection* DAT_011f96a0;
extern "C" char DAT_01017720;
void FUN_0044f570();
struct Setting { void* vftable; void FUN_00404950(); ~Setting() { FUN_00404950(); } };
struct SettingT_INI : Setting {
  ~SettingT_INI() {
    int spare1, spare2, spare3, spare4;
    FUN_0044f570();
    Collection* c = DAT_011f96a0;
    c->Remove(this);
  }
};
class Setting_01017720_011f96a0 : public SettingT_INI {
public: ~Setting_01017720_011f96a0() { vftable=&DAT_01017720; }
};
Setting_01017720_011f96a0 g_0126fae0;