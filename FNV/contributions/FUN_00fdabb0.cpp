extern "C" void __cdecl FUN_0044f570();
extern "C" char DAT_011f3624;
class __declspec(novtable) Setting {
public:
 virtual void Dummy();
 void FUN_00404950();
 __forceinline ~Setting() { reinterpret_cast<Setting*>(&DAT_011f3624)->FUN_00404950(); }
};
class Collection { public: virtual void m0(); virtual void m1(); virtual void Remove(void*); };
extern "C" Collection* DAT_011f96a0;
class Setting_01017720_011f96a0 : public Setting {
public:
 Setting_01017720_011f96a0() {}
 __forceinline ~Setting_01017720_011f96a0() {
   struct Local { Collection* p; int pad[4]; };
   Local loc;
   FUN_0044f570();
   loc.p = DAT_011f96a0;
   loc.p->Remove(this);
 }
};
Setting_01017720_011f96a0 g_011f3624;