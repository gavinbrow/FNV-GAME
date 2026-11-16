// @fnv 0x00fdb7d0
extern "C" void FUN_004de4a0();
extern unsigned char DAT_01022738;
struct INIPrefSettingCollection { virtual void slot0(); virtual void slot1(); virtual void Unregister(void*); };
extern INIPrefSettingCollection* DAT_011f35a0;
struct Setting { void* m_vtable; void FUN_00404950(); ~Setting(){FUN_00404950();} };
struct SettingT : Setting {
  ~SettingT(){
    INIPrefSettingCollection* c;
    int spare0,spare1,spare2,spare3;
    FUN_004de4a0();
    c=DAT_011f35a0;
    c->Unregister(this);
  }
};
struct Setting_00ad9da0 : SettingT {~Setting_00ad9da0(){m_vtable=&DAT_01022738;}};
Setting_00ad9da0 g_011f6e2c;
