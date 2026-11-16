struct SettingName { char* FUN_0044ddc0(); };
struct SettingNode { SettingName** FUN_006815c0(); SettingNode* FUN_00726070(); };
struct SettingStore: SettingNode { bool FUN_008256d0(); void FUN_005ae3d0(SettingName**); };
int __cdecl FUN_00404dc0(const char*,const char*);
extern const char str_0101608c[];
struct Registry { void FUN_0044f770(SettingName*); };
void Registry::FUN_0044f770(SettingName* key) {
AutoMemHelper scope(9, true, str_0101608c, 765);
if (!((SettingStore*)((char*)this+0x10c))->FUN_008256d0()) {
 SettingNode *position = (SettingNode*)((char*)this+0x10c);
 while(position) {
   SettingName *entry=*position->FUN_006815c0();
   if (FUN_00404dc0((const char*)entry->FUN_0044ddc0(),(const char*)key->FUN_0044ddc0())==0) {
    FUN_00c335a0("DEFAULT: Setting key '%s' already used in list.\nSetting keys must be unique.\n",(const char*)key->FUN_0044ddc0());
    return;
   }
   position=position->FUN_00726070();
 }
}
((SettingStore*)((char*)this+0x10c))->FUN_005ae3d0(&key);
}