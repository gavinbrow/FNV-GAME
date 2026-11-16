// @fnv 0x00fdd7d0
extern "C" void FUN_0044f570();
extern unsigned char DAT_01017720;
struct INISettingCollection { virtual void slot0(); virtual void slot1(); virtual void Unregister(void*); };
extern INISettingCollection* DAT_011f96a0;
struct Setting { void* m_vtable; void FUN_00404950(); ~Setting(){FUN_00404950();} };
struct SettingT : Setting {
  ~SettingT(){
    INISettingCollection* c;
    int spare0,spare1,spare2,spare3;
    FUN_0044f570();
    c=DAT_011f96a0;
    c->Unregister(this);
  }
};
class SettingT_GameSettingCollection_ : public SettingT { public: ~SettingT_GameSettingCollection_(){m_vtable=&DAT_01017720;} };
SettingT_GameSettingCollection_ g_01203138;
