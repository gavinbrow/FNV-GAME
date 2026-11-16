extern char str_01012220[];
struct SettingMap{int FUN_004b9ba0();void FUN_006b7f20(int*,int*,int*);};
struct SettingRegistry{virtual void Slot0();virtual void Slot1();virtual void Slot2();virtual void Slot3();virtual void Slot4();virtual bool HandleSetting(int);bool FUN_00405120();};
extern "C" bool __fastcall FUN_00404d30(SettingRegistry*);
extern "C" void __fastcall FUN_00404ee0(S4eb0*);
struct ScopedContext{int previousContext;__forceinline ScopedContext(int context,bool temporary,char* file,int line){reinterpret_cast<S4eb0*>(this)->FUN_00404eb0(context,temporary,file,line);}__forceinline ~ScopedContext(){FUN_00404ee0(reinterpret_cast<S4eb0*>(this));}};
bool SettingRegistry::FUN_00405120(){
int key;ScopedContext memoryGuard(9,true,str_01012220,0x278);
bool isValid=FUN_00404d30(this);
if(isValid){int iterator=reinterpret_cast<SettingMap*>(reinterpret_cast<char*>(this)+0x10c)->FUN_004b9ba0();while(iterator!=0){int value;reinterpret_cast<SettingMap*>(reinterpret_cast<char*>(this)+0x10c)->FUN_006b7f20(&iterator,&key,&value);if(value!=0)isValid=isValid&HandleSetting(value);}}
return isValid;}