struct Items{void FUN_00a64330(unsigned int*);};
typedef unsigned int (__cdecl *ReadFn)(void*,unsigned int*,unsigned int,unsigned int*,unsigned int);
struct Stream{unsigned int unused;unsigned int nread;ReadFn read;};
struct Obj{unsigned int unused;Items items;unsigned int* ptrs;unsigned short cap,n;void FUN_00a89af0(void*);void FUN_00e9f020(char* stream);};
unsigned int FUN_00e9cab0(void*);
void Obj::FUN_00e9f020(char* stream) {
unsigned int num;
FUN_00a89af0(stream);
Stream* in=*(Stream**)(stream+0x24c);
{unsigned int sz=4;in->nread+=in->read(in,&num,4,&sz,1);}
for(unsigned int i=0;i<num;++i){unsigned int item=FUN_00e9cab0(stream);if(item){unsigned int max=n;for(unsigned int j=0;j<max;++j){if(item==ptrs[j])goto found;}items.FUN_00a64330(&item);found:;}}
}