struct NiFileAccessRequest { void* name; unsigned operation,reserved0;void* param;unsigned size,reserved1,result; };
void __cdecl CompleteJob(NiFileAccessRequest*);
unsigned __cdecl FUN_00aa8660(void* p1,unsigned p2,unsigned p3,void* p4) {
 NiFileAccessRequest r;
 r.name=0;r.operation=0;r.param=0;r.reserved1=0;
 r.operation=3;r.name=p4;r.param=p1;r.size=p3;
 CompleteJob(&r);return r.result;
}