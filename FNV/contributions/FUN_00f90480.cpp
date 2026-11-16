// @fnv 0x00f90480
extern "C" char DAT_010741ec, DAT_010741d4, DAT_010741bc, DAT_010741a4;
extern "C" char DAT_01074190, DAT_01074178, DAT_01074160, DAT_01074148, DAT_01074138, DAT_0107411c;
struct CtorShim_0045cfe0 { void FUN_0045cfe0(const char*, int); };
struct SettingProxy {
  unsigned char payload[12];
  __forceinline SettingProxy(const char* s,int flags)
    { reinterpret_cast<CtorShim_0045cfe0*>(this)->FUN_0045cfe0(s,flags); }
  ~SettingProxy() {}
};
SettingProxy screenNames[5] = {
    SettingProxy(&DAT_010741d4,(int)&DAT_010741ec),
    SettingProxy(&DAT_010741a4,(int)&DAT_010741bc),
    SettingProxy(&DAT_01074178,(int)&DAT_01074190),
    SettingProxy(&DAT_01074148,(int)&DAT_01074160),
    SettingProxy(&DAT_0107411c,(int)&DAT_01074138)
};
void FUN_00f90480() {}
