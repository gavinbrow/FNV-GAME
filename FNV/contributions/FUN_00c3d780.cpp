extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);
struct RefObject { void* vtable; long unk04; volatile long refCount; };
struct Array { virtual ~Array(); virtual void* Allocate(unsigned int count); RefObject** data; unsigned int size; unsigned int capacity; void __thiscall FUN_00c3d780(unsigned int reserve, unsigned int count); };
void Array::FUN_00c3d780(unsigned int reserve, unsigned int count) {
 data=0; size=0; capacity=0;
 if(count>reserve) reserve=count;
 if(reserve>0){data=(RefObject**)Allocate(reserve);capacity=reserve;}
 if(count>0){
 unsigned int position;
 RefObject** initializedElement;
 RefObject** destination;
 RefObject* pointer;
 RefObject** array=data;
 for(position=0;position<count;++position){
 destination=array+position;
 initializedElement=destination ? ((*destination=0), (*destination && (pointer=*destination, InterlockedIncrement(&pointer->refCount))), destination) : (RefObject**)0;
 }
 size=count;
 }
}