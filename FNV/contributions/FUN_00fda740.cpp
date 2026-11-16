class INISettingCollection{public:virtual void FUN_00000000();virtual void FUN_00000001();virtual void Remove(void*);};
template<class T>class SettingT{protected:static void EnsureCollection();static T* ms_pCollection;};
extern "C" char DAT_0109545c;extern "C" char DAT_01095434;
class __declspec(novtable) Setting{public:virtual void method();void FUN_00404950();~Setting(){FUN_00404950();}};
class Setting_01017720_011f96a0:public Setting,public SettingT<INISettingCollection>{public:Setting_01017720_011f96a0(const char*,const char*);virtual void method();
__forceinline ~Setting_01017720_011f96a0(){volatile struct Scratch { unsigned a,b,c,d; } x; EnsureCollection(); INISettingCollection* c=ms_pCollection;c->Remove(this);}};
Setting_01017720_011f96a0 g_011f3468(&DAT_0109545c,&DAT_01095434);