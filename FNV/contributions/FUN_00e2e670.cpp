struct FUN_00c90510_Class {void FUN_00c90510();};
struct FUN_00c905b0_Class {void FUN_00c905b0();};
struct C {int a,b,c,d;void** items;int count;void FUN_00e2e670(void* item);};
void C::FUN_00e2e670(void* item) {
 if(item) reinterpret_cast<FUN_00c90510_Class*>(item)->FUN_00c90510();
 int index;
 int i=0;
 if(count>0){
  void** p=items;
  do {if(*p==item){index=i;goto found;} ++i;++p;} while(i<count);
 }
 index=-1;
found:
 if(item) reinterpret_cast<FUN_00c905b0_Class*>(item)->FUN_00c905b0();
 if(index>-1){
  void** target=items+index;
  if(*target) reinterpret_cast<FUN_00c905b0_Class*>(*target)->FUN_00c905b0();
  *target=0;--count;
  int bytes=(count-index)*4;char* dst=reinterpret_cast<char*>(items+index);char* src=reinterpret_cast<char*>(items+index+1);for(int k=0;k<bytes;k+=4)*reinterpret_cast<void**>(dst+k)=*reinterpret_cast<void**>(src+k);
 }
}