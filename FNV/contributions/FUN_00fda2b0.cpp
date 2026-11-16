extern "C" void FUN_0044f570(void);
struct __declspec(novtable) Setting {
 virtual void dummy(); void FUN_00404950(void); ~Setting(){FUN_00404950();}
};
struct INISettingCollection{virtual void dummy0();virtual void dummy1();virtual void Unregister(Setting*);};
extern "C" INISettingCollection *DAT_011f96a0;
struct FUN_0045cf30 : Setting {
 inline void Unregister(){
  INISettingCollection *p=DAT_011f96a0;
  p->Unregister(this);
 }
 virtual ~FUN_0045cf30(){
  int a,b,c,d;
  FUN_0044f570();
  Unregister();
 }
};
extern "C" FUN_0045cf30 DAT_011f33bc;
struct Dummy{~Dummy(){DAT_011f33bc.FUN_0045cf30::~FUN_0045cf30();}};
Dummy g_dummy;