struct Setting;
class INIPrefSettingCollection {public: virtual void Reserved0()=0;virtual void Reserved1()=0;virtual void Unregister(Setting*)=0;};
template<class T> class SettingT {protected: static void EnsureCollection();static T* ms_pCollection;};
struct __declspec(novtable) Setting {virtual void Slot();void FUN_00404950();~Setting(){FUN_00404950();}};
struct FUN_004de370:Setting,SettingT<INIPrefSettingCollection>{virtual void Slot();~FUN_004de370(){EnsureCollection();char unused[12];{INIPrefSettingCollection* coll=ms_pCollection; coll->Unregister(this);}}};
struct __declspec(novtable) Setting_00ad9da0:FUN_004de370{~Setting_00ad9da0(){}};
Setting_00ad9da0 g_011f6e20;