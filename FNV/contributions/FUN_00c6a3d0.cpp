struct Form {int unk0,unk4,unk8; unsigned int flags;};
struct Info {int unk0; volatile char unk4; int unk8,unk12,unk16,unk20,unk24;};
extern void* DAT_011afea4;
Form* __cdecl FUN_00c43490(void* p);
void __cdecl FUN_00c68900(void* p,Info* info,void* g);
bool __cdecl FUN_00c6a3d0(void* p,int b,char c,char d) {
 bool r=false; if(p) {
 Form* f=0; unsigned int bits=0;
 if(!d){f=FUN_00c43490(p);if(f){bits=f->flags;bits &=2;}}
 if(d||(f&&bits)){
 Info info;
unsigned char cc=*(volatile unsigned char*)&c;
 int bb=b;
 info.unk4=cc;
void* g=DAT_011afea4;
 r=true;info.unk0=0;info.unk8=7;info.unk12=bb;
 if(g)FUN_00c68900(p,&info,g);
 }}return r;}