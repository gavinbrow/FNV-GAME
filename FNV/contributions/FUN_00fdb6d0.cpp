class __declspec(novtable) Setting { public: virtual void v0() = 0; void FUN_00404950(); ~Setting(){ FUN_00404950(); } };
class Collection { public: virtual void f0(); virtual void f1(); virtual void remove(Setting*); };
extern "C" void FUN_004de4a0();
extern "C" void* DAT_011f35a0;
struct Holder { Collection* p; unsigned int after[4]; };
class Setting_01022738_011f35a0 : public Setting {
public: virtual void v0();
 Setting_01022738_011f35a0(const char*, float) {}
 __forceinline ~Setting_01022738_011f35a0() {
   Holder h;
   FUN_004de4a0();
   h.p=(Collection*)DAT_011f35a0;
   h.p->remove(this);
 }
};
extern "C" char DAT_010a3758;
Setting_01022738_011f35a0 g_011f6e14(&DAT_010a3758,1.0f);