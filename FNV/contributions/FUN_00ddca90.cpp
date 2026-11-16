extern int g_callbackContext;
struct Target {
 virtual void f00(); virtual void f04(); virtual void f08(); virtual void f0c();
 virtual void f10(); virtual void f14(); virtual void f18(); virtual void f1c();
 virtual void f20(); virtual void f24(); virtual void f28(); virtual void f2c();
 virtual int invoke(int,int,int,int,int);
};
struct Adapter { int FUN_00ddca90(int,int,int,int,int); };
struct AdapterHeader { Target* target; unsigned int flags; };
int Adapter::FUN_00ddca90(int a, int b, int c, int d, int context) {
 AdapterHeader* header = reinterpret_cast<AdapterHeader*>(reinterpret_cast<char*>(this)-sizeof(AdapterHeader));
 return header->target->invoke(a,b,c,d,g_callbackContext);
}
