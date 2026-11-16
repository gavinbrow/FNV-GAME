extern "C" void* DAT_010d7510[];
struct FUN_00dc8030_Allocator { virtual void slot0();virtual void* Allocate(unsigned int bytes); };
struct FUN_00dc8030_Memory {int unk00,unk04,unk08,unk0c;FUN_00dc8030_Allocator* allocator;};
extern "C" FUN_00dc8030_Memory* __cdecl FUN_00c85750();
struct FUN_00dc7fd0_Class {int unk00;};
extern "C" FUN_00dc7fd0_Class* __fastcall FUN_00dc7fd0(FUN_00dc7fd0_Class*);
struct FUN_00dc8030_Class {
void** vtable;unsigned short allocationSize,refCount;FUN_00dc7fd0_Class* owned;
FUN_00dc8030_Class* __thiscall FUN_00dc8030();
};
FUN_00dc8030_Class* __thiscall FUN_00dc8030_Class::FUN_00dc8030(){
refCount=1;vtable=DAT_010d7510;
FUN_00dc8030_Memory* sys=FUN_00c85750();FUN_00dc8030_Allocator* allocator=sys->allocator;
FUN_00dc7fd0_Class* p=(FUN_00dc7fd0_Class*)allocator->Allocate(0x88);
owned = p ? FUN_00dc7fd0(p) : (FUN_00dc7fd0_Class*)0;
return this;
}