
extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
struct NiRefObject {virtual void v00();virtual void DeleteThis();volatile long refCount;};
struct NiPointer {NiRefObject* ptr;explicit NiPointer(NiRefObject* p):ptr(p){if(p){InterlockedIncrement(&p->refCount);if(!InterlockedDecrement(&p->refCount))p->DeleteThis();}}};
struct RefArray {void* unk00;NiRefObject** entries;unsigned short capacity;unsigned short size;unsigned short count;NiPointer FUN_00c20fd0();};

NiPointer RefArray::FUN_00c20fd0(){
 if (!size) return NiPointer(0);
 NiRefObject* object=entries[--size];
 if(object) InterlockedIncrement(&object->refCount);
 NiRefObject** slot=entries+size;
 NiRefObject* old=*slot;
 if(old){if(!InterlockedDecrement(&old->refCount))old->DeleteThis();*slot=0;}
 const bool& x = object != 0; if(x) --count;
 return NiPointer(object);
}