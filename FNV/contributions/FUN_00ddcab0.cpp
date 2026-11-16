extern int DAT_01269cdc;
struct VirtualReceiver {
 virtual int method0(int,int,int);
 virtual int method1(int,int,int);
 virtual int method2(int,int,int);
 virtual int method3(int,int,int);
 virtual int method4(int,int,int);
 virtual int method5(int,int,int);
 virtual int method6(int,int,int);
 virtual int method7(int,int,int);
 virtual int method8(int,int,int);
 virtual int method9(int,int,int);
 virtual int method10(int,int,int);
 virtual int method11(int,int,int);
 virtual int method12(int,int,int);
 virtual int method13(int,int,int);
};
struct WrapperObject { int __thiscall FUN_00ddcab0(int first,int second,int third); };
int WrapperObject::FUN_00ddcab0(int first,int second,int third) {
 VirtualReceiver* receiver=*(VirtualReceiver**)((char*)this - 8);
 return receiver->method13(first,second,DAT_01269cdc);
}