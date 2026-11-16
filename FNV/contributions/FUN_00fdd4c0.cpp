class __declspec(novtable) Setting { public: virtual void v0() = 0; void FUN_00404950(); ~Setting(){ FUN_00404950(); } };
class Collection { public: virtual void f0(); virtual void f1(); virtual void remove(Setting*); };
extern "C" void FUN_0044f570();
extern "C" void* DAT_011f96a0;
struct Holder { Collection* p; unsigned int after[4]; };
class Setting_01017720_011f96a0 : public Setting {
public: virtual void v0();
 Setting_01017720_011f96a0(const char*,int) {}
 __forceinline ~Setting_01017720_011f96a0() {
   Holder h;
   FUN_0044f570();
   h.p=(Collection*)DAT_011f96a0;
   h.p->remove(this);
 }
};
extern "C" char DAT_010c179c;
Setting_01017720_011f96a0 g_01202db4(&DAT_010c179c,20);