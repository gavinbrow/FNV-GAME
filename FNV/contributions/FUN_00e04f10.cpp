struct FUN_00e04f10_Resource { int refs; };
extern "C" void __fastcall FUN_00c90510(FUN_00e04f10_Resource* resource);
struct FUN_00e04f10_Manager {
virtual void slot00();
virtual void slot04();
virtual void slot08();
virtual FUN_00e04f10_Resource* GetSecond();
virtual FUN_00e04f10_Resource* GetFirst();
};
extern "C" FUN_00e04f10_Manager* DAT_01268b08;
extern "C" void* DAT_010ea4dc[];
struct FUN_00e04f10_Values { int first,second; };
class FUN_00e04f10_Class {
public:
 void** vtable;
 unsigned short unk04,refCount;
 FUN_00e04f10_Values values;
 FUN_00e04f10_Resource* first;
 FUN_00e04f10_Resource* second;
 FUN_00e04f10_Class* FUN_00e04f10(const FUN_00e04f10_Values* init);
};
FUN_00e04f10_Class* FUN_00e04f10_Class::FUN_00e04f10(const FUN_00e04f10_Values* init) {
refCount=1;
vtable=DAT_010ea4dc;
values=*init;
FUN_00e04f10_Resource* resource=DAT_01268b08->GetFirst();
if(resource)FUN_00c90510(resource);
first=resource;
resource=DAT_01268b08->GetSecond();
if(resource)FUN_00c90510(resource);
second=resource;
return this;
}