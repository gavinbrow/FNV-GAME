struct Entry {virtual void m00();virtual void m04();virtual void m08();virtual void m0c();virtual void m10();virtual void m14();virtual void m18();virtual void m1c();virtual void m20();virtual void m24();virtual void m28();virtual void m2c();virtual void m30();virtual void process(int);};
struct MemoryManager{virtual void m00();virtual void m04();virtual void m08();virtual void m0c();virtual void freeBlock(void*,int);};
struct MemoryRouter{void* vt;int unk04;int unk08;int unk0c;MemoryManager* manager;};
struct EntryArray{Entry** data;int size;int capacityAndFlags;};
void __stdcall FUN_00e2e2e0(EntryArray*);MemoryRouter* __cdecl FUN_00c85750();
void __stdcall FUN_00e2e960(int x){
 EntryArray a;a.data=0;a.size=0;a.capacityAndFlags=0x80000000;
 FUN_00e2e2e0(&a);
 for(int i=0;i<a.size;++i)a.data[i]->process(x);
 MemoryRouter* r=FUN_00c85750();
 int cap=a.capacityAndFlags;
 {MemoryManager* m=r->manager; a.size=0; if(!(cap&0x80000000))m->freeBlock(a.data,(cap&0x3fffffff)*4);}
}