extern int DAT_010d62fc;
struct Source {virtual void a(); virtual void b(); virtual void c(); virtual void d(); virtual void* vf10(void*);};
struct Allocator {virtual void a(); virtual void* allocate(unsigned int);};
struct Router {int a,b,c,d; Allocator* allocator;};
Router* __cdecl FUN_00c85750();
struct Index {void* __thiscall FUN_00d87800(void*, void*); void __thiscall FUN_00d874d0(void*,void*);};
struct Record {void* type; unsigned short byteSize; unsigned short flags; unsigned int state; void* reference; void* owner;};
struct Object {int a,b;Source* source;int d;Index index; Record* __thiscall FUN_00dbb520(void*);};
Record* Object::FUN_00dbb520(void* key) {
 void* reference;
 if (key) {Record* existing=(Record*)index.FUN_00d87800(key,0);if(existing)return existing;reference=source->vf10(key);}
 else reference=0;
 Router* router=FUN_00c85750();
 Record* record=(Record*)router->allocator->allocate(20);
record->byteSize = 20;
record->flags = 0;
record->state = 0;
 record->type=&DAT_010d62fc;
 record->reference=reference;
 record->owner=this;
 index.FUN_00d874d0(key,record);
 return record;
}