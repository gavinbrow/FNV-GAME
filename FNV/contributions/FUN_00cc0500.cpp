#include "h_74712c1d3c73.h"
struct Param4 { int value; };
struct D274C0Child {
void* m_vtable;unsigned short m_memorySize;unsigned short m_referenceCount;int unk08,unk0c,unk10,unk14,unk18;
D274C0Child* __thiscall FUN_00d274c0(int first,int second,Param4 third);
};
struct FUN_00cc0500_Class {
void* m_vtable;unsigned short m_memorySize;unsigned short m_referenceCount;D274C0Child* m_child;
FUN_00cc0500_Class* __thiscall FUN_00cc0500(int first,int second,Param4 third);
};
FUN_00cc0500_Class* FUN_00cc0500_Class::FUN_00cc0500(int first,int second,Param4 third)
{
m_referenceCount=1;m_vtable=&DAT_010c9314;
D274C0Child* child=static_cast<D274C0Child*>(FUN_00c85750()->heap().blockAlloc(28));
child->m_memorySize=28;
m_child=child->FUN_00d274c0(first,second,third);
return this;
}