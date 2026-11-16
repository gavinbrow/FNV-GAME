class Obj {public:virtual void v0();virtual void v1();virtual const char* getName();virtual void v3();virtual void* getKey();};
struct Find{char* FUN_00d874b0(char*,int);};struct Add{void FUN_00d874d0(const char*,int);};
struct Map{void FUN_00dc9ec0(void*,Obj**);};
struct Registry{int a,b,c,d;Map map;int FUN_00d87580(const char*);void FUN_00dca820(Obj* volatile obj);};
void Registry::FUN_00dca820(Obj* volatile obj){
 Obj* const current=obj;
 void* key=current->getKey();
 const char* name=current->getName();
 int it=FUN_00d87580(name);
 char valid;
 reinterpret_cast<Find*>(this)->FUN_00d874b0(&valid,it);
 if(!valid){
  const char* n2=current->getName();
  reinterpret_cast<Add*>(this)->FUN_00d874d0(n2,(int)current);
  if(key) map.FUN_00dc9ec0(key,const_cast<Obj**>(&obj));
 }
}