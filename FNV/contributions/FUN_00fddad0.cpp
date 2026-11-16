extern "C" unsigned char DAT_01017720;
extern "C" void FUN_0044f570();
class Setting {public: void FUN_00404950(); ~Setting(){FUN_00404950();}};
class INISettingCollection {public: virtual void f0();virtual void f1();virtual void RemoveSetting(Setting*);};
extern INISettingCollection* DAT_011f96a0;
class SettingT : public Setting {
public:
 ~SettingT() {
  INISettingCollection* c; int spare0,spare1,spare2,spare3;
  FUN_0044f570();
  c=DAT_011f96a0;
  c->RemoveSetting(this);
 }
};
class Setting_01017720_011f96a0 : public SettingT {
public:
 Setting_01017720_011f96a0(const char*, bool);
 ~Setting_01017720_011f96a0() {*reinterpret_cast<void**>(this)=&DAT_01017720;}
};
extern const char s_010c291c[];
Setting_01017720_011f96a0 g_01203188(s_010c291c,false);
