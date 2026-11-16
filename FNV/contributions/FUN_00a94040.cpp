struct FNV_UpdateFlags{float time;unsigned char shouldActivate;};
struct FNV_Color4{unsigned int first,second,third;float fourth;};
extern FNV_Color4 DAT_011f4288;
extern "C" void __stdcall FUN_004eff50(FNV_UpdateFlags*,unsigned int);
struct FNV_SwitchVirtual:NiAVObject{virtual void f35();virtual void f36();virtual void f37();virtual void f38();virtual void f39();virtual void f40();virtual void f41();virtual void f42();virtual void f43();virtual void f44();virtual void NotifyUpdated(FNV_UpdateFlags*);};
struct FNV_ChildVirtual:NiAVObject{virtual void f35();virtual void f36();virtual void f37();virtual void f38();virtual void f39();virtual void NotifySelected(FNV_UpdateFlags*,unsigned int);};
struct FNV_SwitchTracker{void FUN_0096ae90(int,unsigned int*);};
struct FUN_00a94040_shell:NiSwitchNode{
float m_time;unsigned int m_revision;FNV_SwitchTracker m_tracker;
void FUN_00a5dd70(FNV_UpdateFlags*,unsigned int);
void FUN_00a94040(FNV_UpdateFlags*,unsigned int);
};
void FUN_00a94040_shell::FUN_00a94040(FNV_UpdateFlags* update,unsigned int flags){
unsigned short& state=*reinterpret_cast<unsigned short*>(&m_0ac);
if(update->shouldActivate)state|=2;else state&=~2u;
m_time=update->time;
if(m_0ac&1){
++m_revision;
unsigned int* count=&m_revision;
if(update->shouldActivate)FUN_004eff50(update,1);
reinterpret_cast<FNV_SwitchVirtual*>(this)->NotifyUpdated(update);
if((int)m_0b0>=0){
FNV_ChildVirtual* child=reinterpret_cast<FNV_ChildVirtual**>(m_0a0)[(int)m_0b0];
if(child){
child->NotifySelected(update,flags);
m_tracker.FUN_0096ae90((int)m_0b0,count);
NiObject* raw=reinterpret_cast<NiObject*>(child);
FNV_Color4* color=raw->m_020?reinterpret_cast<FNV_Color4*>(raw->m_020):&DAT_011f4288;
FNV_Color4* out=reinterpret_cast<FNV_Color4*>(m_020);float alpha=color->fourth;out->first=color->first;out->second=color->second;out->third=color->third;out->fourth=alpha;}}}else{FUN_00a5dd70(update,flags);}}