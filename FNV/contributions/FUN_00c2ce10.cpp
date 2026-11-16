struct State { int value; State(int value):value(value){} };
struct Callback{int unk00;int count;int(__cdecl*invoke)(Callback*,void**,int,const State&,int);};
void __stdcall FUN_00c32120(void*);
struct Subobject{void __thiscall FUN_00a59be0(void*);};
struct FUN_00c2ce10_owner{void __thiscall FUN_00c2ce10(void*object);};
void FUN_00c2ce10_owner::FUN_00c2ce10(void*object){
void*original=object;FUN_00c32120(original);
Callback*cb=*reinterpret_cast<Callback**>(static_cast<char*>(original)+0x24c);

cb->count+=cb->invoke(cb,&object,1,State(1),1);
*reinterpret_cast<unsigned char*>(reinterpret_cast<char*>(this)+0x30)=
*reinterpret_cast<unsigned char*>(&object)!=0;
reinterpret_cast<Subobject*>(reinterpret_cast<char*>(this)+0x34)->FUN_00a59be0(original);
}