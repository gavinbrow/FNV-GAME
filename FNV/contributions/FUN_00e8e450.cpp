__declspec(nothrow) int FUN_00aa1360(const char*,const char*);
__declspec(dllimport) __declspec(nothrow) long __stdcall InterlockedDecrement(volatile long*);
__declspec(dllimport) __declspec(nothrow) long __stdcall InterlockedIncrement(volatile long*);
extern char* EmptyFS;
__declspec(nothrow) inline long NiAtomicDecrement(volatile long* value) { return InterlockedDecrement(value); }
struct StringHeader { volatile long refs; unsigned int length; };
struct NiGlobalStringTable {
 __declspec(nothrow) static char* AddString(const char*);
 __declspec(nothrow) static volatile long* GetRefCount(char*& h) { return &((StringHeader*)h - 1)->refs; }
 __declspec(nothrow) static void IncRefCount(char*& h) { if(h==EmptyFS)return; InterlockedIncrement(GetRefCount(h)); }
 __declspec(nothrow) static void DecRefCount(char*& h) { if(h==EmptyFS)return; volatile long* count=GetRefCount(h); NiAtomicDecrement(count); }
};
class NiFixedString {
public:
 char* data;
 __declspec(nothrow) NiFixedString() : data(EmptyFS) {}
 __declspec(nothrow) NiFixedString(const char* text);
 __declspec(nothrow) ~NiFixedString();
 NiFixedString& operator=(const char* text) {
  if(data!=text) { char* old=data; data=NiGlobalStringTable::AddString(text); if(old!=EmptyFS) InterlockedDecrement(&((StringHeader*)old - 1)->refs); }
  return *this;
 }
 NiFixedString& operator=(const NiFixedString& other) {
  char* incoming = other.data;
  if (data != incoming) {
    NiGlobalStringTable::IncRefCount(incoming);
    char* outgoing = data;
    NiGlobalStringTable::DecRefCount(outgoing);
    data = incoming;
  }
  return *this;
 }
 bool operator==(const char* text) const {
  if(data==text)return true;
  if(!text || !data)return false;
  return FUN_00aa1360(data,text)==0;
 }
};



__declspec(nothrow) NiFixedString::NiFixedString(const char* text) { if(!text) data=EmptyFS; else data=NiGlobalStringTable::AddString(text); }
__declspec(nothrow) NiFixedString::~NiFixedString() { NiGlobalStringTable::DecRefCount(data); }

struct W20Profiles {
 NiFixedString* data;
 unsigned int capacity, count, unk0c, unk10;
 __declspec(nothrow) void FUN_00e8e290(unsigned int);
 __declspec(nothrow) void FUN_00e8e330(const NiFixedString& value) {
  if(count==capacity) FUN_00e8e290(capacity>0 ? capacity*2 : 1);
  data[count++]=value;
 }
};
struct W20Base {
 virtual void foo();
 unsigned int unk04,unk08,unk0c,unk10,unk14;
 NiFixedString name;
 unsigned int unk1c,unk20;
 NiFixedString profile;
 W20Profiles profiles;
 __declspec(nothrow) W20Base(int,int,int);
 __declspec(nothrow) void FUN_00ee8af0(const NiFixedString&);
 __declspec(nothrow) void FUN_00ee9350();
};
struct FUN_00e8e450 : W20Base {
 int type;
 bool flag;
 NiFixedString suffix;
 virtual void foo();
 __declspec(nothrow) FUN_00e8e450(int,const char*,int,const NiFixedString&,const char*,int,bool,int,bool);
};
__declspec(nothrow) void FUN_00a305b0(char*,unsigned int,const char*,...);
__declspec(nothrow) FUN_00e8e450::FUN_00e8e450(int a,const char* source,int kind,const NiFixedString& requested,const char* path,int b,bool use,int c,bool load)
 : W20Base(a,b,c)
{
 flag=use;
 type=kind;
 suffix=path;
 char filename[260];
 FUN_00a305b0(filename,260,"%s_%s_%s.cache",path,requested.data,"DX9");
 name=filename;
 FUN_00ee8af0(source);
 profile=requested;
 if(kind==0) {
  if(profile=="vs_1_1") { profiles.FUN_00e8e330("vs_1_1"); }
  else if(profile=="vs_2_0") { profiles.FUN_00e8e330("vs_2_0"); profiles.FUN_00e8e330("vs_1_1"); }
  else if(profile=="vs_2_a") { profiles.FUN_00e8e330(NiFixedString("vs_2_a")); profiles.FUN_00e8e330(NiFixedString("vs_2_0")); profiles.FUN_00e8e330(NiFixedString("vs_1_1")); }
  else if(profile=="vs_3_0") { profiles.FUN_00e8e330(NiFixedString("vs_3_0")); profiles.FUN_00e8e330(NiFixedString("vs_2_a")); profiles.FUN_00e8e330(NiFixedString("vs_2_0")); profiles.FUN_00e8e330(NiFixedString("vs_1_1")); }
 } else if(kind==2) {
  if(profile=="ps_1_1") profiles.FUN_00e8e330(NiFixedString("ps_1_1"));
  else if(profile=="ps_1_2") { profiles.FUN_00e8e330(NiFixedString("ps_1_2")); profiles.FUN_00e8e330(NiFixedString("ps_1_1")); }
  else if(profile=="ps_1_3") { profiles.FUN_00e8e330(NiFixedString("ps_1_3")); profiles.FUN_00e8e330(NiFixedString("ps_1_2")); profiles.FUN_00e8e330(NiFixedString("ps_1_1")); }
  else if(profile=="ps_1_4") { profiles.FUN_00e8e330(NiFixedString("ps_1_4")); profiles.FUN_00e8e330(NiFixedString("ps_1_3")); profiles.FUN_00e8e330(NiFixedString("ps_1_2")); profiles.FUN_00e8e330(NiFixedString("ps_1_1")); }
  else if(profile=="ps_2_0") { profiles.FUN_00e8e330(NiFixedString("ps_2_0")); profiles.FUN_00e8e330(NiFixedString("ps_1_4")); profiles.FUN_00e8e330(NiFixedString("ps_1_3")); profiles.FUN_00e8e330(NiFixedString("ps_1_2")); profiles.FUN_00e8e330(NiFixedString("ps_1_1")); }
  else if(profile=="ps_2_a") { profiles.FUN_00e8e330(NiFixedString("ps_2_a")); profiles.FUN_00e8e330(NiFixedString("ps_2_0")); profiles.FUN_00e8e330(NiFixedString("ps_1_4")); profiles.FUN_00e8e330(NiFixedString("ps_1_3")); profiles.FUN_00e8e330(NiFixedString("ps_1_2")); profiles.FUN_00e8e330(NiFixedString("ps_1_1")); }
  else if(profile=="ps_2_b") { profiles.FUN_00e8e330(NiFixedString("ps_2_b")); profiles.FUN_00e8e330(NiFixedString("ps_2_0")); profiles.FUN_00e8e330(NiFixedString("ps_1_4")); profiles.FUN_00e8e330(NiFixedString("ps_1_3")); profiles.FUN_00e8e330(NiFixedString("ps_1_2")); profiles.FUN_00e8e330(NiFixedString("ps_1_1")); }
  else if(profile=="ps_3_0") { profiles.FUN_00e8e330(NiFixedString("ps_3_0")); profiles.FUN_00e8e330(NiFixedString("ps_2_a")); profiles.FUN_00e8e330(NiFixedString("ps_2_0")); profiles.FUN_00e8e330(NiFixedString("ps_1_4")); profiles.FUN_00e8e330(NiFixedString("ps_1_3")); profiles.FUN_00e8e330(NiFixedString("ps_1_2")); profiles.FUN_00e8e330(NiFixedString("ps_1_1")); }
 }
 if(load && source) FUN_00ee9350();
}
