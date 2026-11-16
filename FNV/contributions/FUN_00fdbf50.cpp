// @fnv 0x00fdbf50
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
struct Setting_01017720_011f96a0 : SettingT {~Setting_01017720_011f96a0(){m_vtable=&DAT_01017720;}};
Setting_01017720_011f96a0 g_011f6ee0;
