
struct Allocator { virtual void allocatorOperation0();virtual void allocatorOperation1();virtual void deallocateObject(void* object,unsigned short allocatorTag);virtual void allocatorOperation3();virtual void deallocateArray(void* buffer,unsigned int bytes); };
struct MemoryRouter {int unknown00,unknown04,unknown08,unknown0c;Allocator* allocator;};
MemoryRouter* __cdecl FUN_00c85750();
extern char DAT_0102e388;
struct HavokArrayOwner {void* vtable;unsigned short allocatorTag;unsigned short unknown06;void* data;unsigned int size;int capacityFlags;HavokArrayOwner* FUN_00e015d0(unsigned int deletionFlags);};
HavokArrayOwner* HavokArrayOwner::FUN_00e015d0(unsigned int deletionFlags)
{
 MemoryRouter* router=FUN_00c85750();
 Allocator* allocator=router->allocator;
 int previousCapacity=capacityFlags;
 size=0;
 if((previousCapacity & 0x80000000)==0){allocator->deallocateArray(data,(previousCapacity & 0x3fffffff)*4);}
 data=0;capacityFlags=0x80000000;vtable=&DAT_0102e388;
if(deletionFlags&1) { MemoryRouter* router2=FUN_00c85750();router2->allocator->deallocateObject(this,allocatorTag); }
return this;
}