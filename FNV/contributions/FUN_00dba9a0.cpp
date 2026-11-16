struct Interface { virtual void f0();
virtual void f1();
virtual void f2();
virtual void f3();
virtual void f4();
virtual void f5();
virtual void f6();
virtual void f7();
virtual void f8();
virtual void f9();
virtual void f10();
virtual void f11();
virtual void f12();
virtual void f13(); virtual void f14(void* first, unsigned int second); };
struct FUN_00dba9a0_cls { Interface* ptr; void* p1; void FUN_00dba9a0(unsigned int param); };
void FUN_00dba9a0_cls::FUN_00dba9a0(unsigned int param) { ptr->f14(p1, param); }
