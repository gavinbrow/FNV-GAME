char* __cdecl FUN_00cb1410(const char*);
struct Crux53_StringMap{void* FUN_00d87800(const char*,int);void* FUN_00d874d0(void*,void*);};
struct Crux53_MapBody{int a00,a04,a08,a0c,a10,a14,a18,a1c,a20,a24,a28,a2c,a30,a34,a38,a3c,a40,a44,a48;Crux53_StringMap map4c;void* intern(const char* key){
if(key){void* value=map4c.FUN_00d87800(key,0);if(!value){value=FUN_00cb1410(key);map4c.FUN_00d874d0(value,value);}return value;}return 0;}};
struct Crux53_MapInner{void* a00;void* a04;Crux53_MapBody* a08;};
struct Crux53_MapOuter{void* a00;void* a04;void* a08;Crux53_MapInner* a0c;};
struct Crux53_Entry{void* key;void* obj;};
struct Crux53_Owner{void* a00;void* a04;void* a08;Crux53_Entry* entries;int count;void* a14;Crux53_MapOuter* outer;
int FUN_00dcb550(void*);int FUN_00dcb5d0(const char*);};
int Crux53_Owner::FUN_00dcb5d0(const char* key){
void* value=outer->a0c->a08->intern(key);
int i=0;
if(count>0){
 Crux53_Entry* e=entries;
 do{if(e->key==value){if(i!=-1)return i;break;}++i;++e;}while(i<count);
}
return FUN_00dcb550(value);
}