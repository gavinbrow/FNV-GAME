// @fnv 0x00fdbbd0
extern "C" void FUN_0044f570();
extern unsigned char DAT_01017720;
struct INISettingCollection { virtual void slot0(); virtual void slot1(); virtual void Unregister(void*); };
extern INISettingCollection* DAT_011f96a0;
struct ExternalSetting { void* m_vtable; void FUN_00404950(); };
extern ExternalSetting DAT_011f6e8c;
struct Setting { ~Setting(){DAT_011f6e8c.FUN_00404950();} };
struct SettingT : Setting {
  ~SettingT(){
    INISettingCollection* c; int spare0,spare1,spare2,spare3;
    FUN_0044f570();
    c=DAT_011f96a0;
    c->Unregister(&DAT_011f6e8c);
  }
};
struct GlobalSettingFinalizer : SettingT {
 ~GlobalSettingFinalizer(){DAT_011f6e8c.m_vtable=&DAT_01017720;}
};
GlobalSettingFinalizer g_011f6e8c_finalizer;
