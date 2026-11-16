struct Buffers {char* first;char* second;char* third;char* fourth;};
struct Obj{int a,b,c,byte_size,d;unsigned short count;void FUN_00e42b00(char* base,int unused,Buffers* out) const;};
inline int align16(int n){return (n+15)&~15;}
void Obj::FUN_00e42b00(char* base,int unused,Buffers* out) const {
 int n=count;int sz=byte_size;
 char* p=base+align16(n*80);out->second=p;p+=align16(n*96);char* q=p;p+=align16(sz);out->first=base;out->fourth=p;out->third=q;
}